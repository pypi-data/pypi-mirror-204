import logging
import warnings

import lightkurve as lk
import numpy as np
import pandas as pd
from astropy.stats import mad_std
from astropy.utils.exceptions import AstropyUserWarning
from astroquery.exceptions import TableParseError
from astroquery.vizier import Vizier
from astroquery.jplhorizons import Horizons
from astroquery.mast import Catalogs
from astroquery.simbad import Simbad
from matplotlib import pyplot as plt
from matplotlib.offsetbox import AnchoredText
from matplotlib.ticker import MaxNLocator
from wotan import flatten

from .utils import (
    CANDIDATES_COLUMNS,
    STELLAR_PARAMETER_COLUMNS,
    calculate_stellar_luminosity,
    extend,
    fill_gaps,
    find_consecutive,
    get_flare_probability,
    query_gaia_dr3_id,
)

logging.getLogger("astroquery").setLevel(logging.WARNING)

CUSTOM_SIMBAD = Simbad()
CUSTOM_SIMBAD.add_votable_fields("otype")
CUSTOM_SIMBAD.add_votable_fields("otypes")

VIZIER = Vizier(columns=["Plx", "Gmag", "BP-RP"])

EXCLUDED_OTYPES = ["CataclyV*", "CataclyV*_Candidate", "Nova", "Nova_Candidate"]


def load_from_lightkurve(lc):
    with warnings.catch_warnings():
        warnings.simplefilter("error", category=lk.LightkurveWarning)

        try:
            lc.meta["ZERO_CENTERED"] = False
            negative_ratio = (lc.flux.value < -30).nonzero()[0].size / lc.flux.nonzero()[0].size
            if negative_ratio > 0.1:
                raise lk.LightkurveWarning
            lc = lc.normalize()
        except lk.LightkurveWarning:
            try:
                lc = lc.select_flux("sap_flux").normalize()
            except lk.LightkurveWarning:
                lc.meta["ZERO_CENTERED"] = True
                lc.flux += lc.flux.std() - lc.flux.min()
                lc = lc.normalize()

    flc = FlareLightCurve(lc)

    return flc


class FlareLightCurve(lk.LightCurve):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.meta["stellar_parameters"] = None
        self.meta["candidates"] = None

    def _generate_model(self):
        """
        Generate a model for the light curve.

        This method generates a model for the light curve by computing a percentile-based
        representation of the flux values.

        Returns
        -------
        model_flux : ndarray
            The model flux values.
        """

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            pg = self.to_periodogram()
            period = pg.period_at_max_power.value
            snr = pg.max_power / np.nanmedian(pg.power)

            if period < 10 and snr > 5:
                pg = self.to_periodogram(
                    minimum_period=max(period - 0.2, 0.01),
                    maximum_period=period + 0.2,
                    oversample_factor=1000,
                )
                period = pg.period_at_max_power.value
            else:
                period = -999

            self.meta["PERIOD"] = period

        if 0.05 < period < 2:
            period_array = np.array([1, 2, 4]) * period
            std_array = np.zeros_like(period_array)
            folded_lc_list = []
            trend_folded_flux_list = []

            for i, period in enumerate(period_array):
                folded_lc = self.fold(period)
                detrended_folded_flux, trend_folded_flux = flatten(
                    folded_lc.time.value,
                    folded_lc.flux,
                    method="median",
                    window_length=period / 50,
                    return_trend=True,
                )
                std_array[i] = np.nanstd(detrended_folded_flux)
                folded_lc_list.append(folded_lc)
                trend_folded_flux_list.append(trend_folded_flux)

            std_array *= 0.75 ** np.arange(len(period_array))[::-1]
            index = std_array.argmin()
            self.meta["PERIOD"] = period_array[index]
            trend_folded_flux = trend_folded_flux_list[index]
            folded_lc = folded_lc_list[index]

            return trend_folded_flux[folded_lc.time_original.argsort()] - 1
        return 0

    def _mask_eclipse(self):
        """
        Mask the eclipses in the light curve.

        This method masks the eclipses present in the light curve by setting the corresponding
        flux values to NaN (Not a Number).
        """

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=AstropyUserWarning)

            sigma = mad_std(self.flux, ignore_nan=True)
            eclipse_mask = self.flux < np.nanmedian(self.flux) - 3 * sigma
            if hasattr(self.flux, "mask"):
                eclipse_mask = np.logical_xor(eclipse_mask, self.flux.mask)

            i_start_array, i_stop_array = find_consecutive(
                np.nonzero(eclipse_mask)[0],
                3,
                gap=1.2 * self.meta["TIMEDEL"],
                data=self.time.value,
            )

            lc = self.copy()
            if i_start_array is not None:
                if i_start_array.size > 3 and lc.time.value[i_start_array[0]] < lc.time.value[i_stop_array[-1]] - 10:
                    for i in range(i_start_array.size):
                        t_start = self.time.value[i_start_array[i]]
                        t_stop = self.time.value[i_stop_array[i]]
                        duration = t_stop - t_start
                        t_start_ext, t_stop_ext = extend(
                            lc.time.value,
                            (lc.flux - 1) / sigma,
                            t_start,
                            t_stop,
                            duration,
                            n_sigma=0,
                            mode=-1,
                        )
                        lc.flux[(self.time.value >= t_start_ext) & (self.time.value <= t_stop_ext)] = np.nan

            self.meta["eclipse_mask"] = np.isnan(lc.flux)

        return lc

    def _extend_multiple_events(self, start_indexes, stop_indexes, max_extend_indexes=45):
        start_ext_indexes = np.zeros_like(start_indexes)
        stop_ext_indexes = np.zeros_like(stop_indexes)

        lc = self.copy()
        lc.flux[self.eclipse_mask] = np.nan
        lc = lc.remove_nans()

        max_extend_time = (max_extend_indexes + 0.2) * self.meta["TIMEDEL"]

        for i, (start_index, stop_index) in enumerate(zip(start_indexes, stop_indexes)):
            t_start = self.time.value[start_index]
            t_stop = self.time.value[stop_index]

            t_start_ext, t_stop_ext = extend(
                lc.time.value,
                lc.standardized_flux,
                t_start,
                t_stop,
                max_extend_time,
                n_right=2,
            )

            start_ext_indexes[i] = np.nonzero(self.time.value == t_start_ext)[0][0]
            stop_ext_indexes[i] = np.nonzero(self.time.value == t_stop_ext)[0][0]

        overlap_indexes = np.nonzero(start_ext_indexes[1:] <= stop_ext_indexes[:-1])[0] + 1
        overlap_start, overlap_stop = find_consecutive(overlap_indexes, 1)

        if overlap_start is not None:
            stop_ext_indexes[overlap_start - 1] = stop_ext_indexes[overlap_stop]
            start_ext_indexes = np.delete(start_ext_indexes, overlap_indexes)
            stop_ext_indexes = np.delete(stop_ext_indexes, overlap_indexes)

        return start_ext_indexes, stop_ext_indexes

    def _standardize(self):
        """
        Standardize the detrended light curve.

        This method standardizes the detrended light curve by dividing the difference between the
        flux and 1 by the rolling standard deviation. It then adds the rolling standard deviation
        and the standardized flux as new columns to the class.
        """

        flux_series = pd.Series(self.detrended_flux.value, index=pd.DatetimeIndex(self.time.datetime))

        rolling_window = flux_series.rolling(pd.Timedelta(2, unit="d"), center=True)
        rolling_std = rolling_window.apply(mad_std, kwargs={"ignore_nan": True})
        rolling_std[np.isnan(self.detrended_flux.value)] = np.nan

        standardized_flux = (self.detrended_flux.value - 1) / rolling_std

        self.add_columns([rolling_std, standardized_flux], names=["rolling_std", "standardized_flux"])

    def _is_sso(self, i_peak: int, radius: float = 8):
        """
        Check if a candidate is caused by a Solar System Object (SSO) encounter.

        Parameters
        ----------
        i_peak : int
            The index of the peak in the candidate light curve.
        radius : float, optional
            The search radius for SSOs, in arcseconds. Default is 8.

        Returns
        -------
        bool
            True if the candidate is caused by an SSO encounter, False otherwise.
        """

        mask = np.zeros_like(self.time, dtype=bool)
        mask[i_peak] = True

        try:
            res = self.query_solar_system_objects(cadence_mask=mask, radius=radius * 21 / 3600, show_progress=False)
        except OSError:
            res = self.query_solar_system_objects(
                cadence_mask=mask,
                radius=radius * 21 / 3600,
                cache=False,
                show_progress=False,
            )

        if res is not None:
            ap_mag = np.zeros(len(res))
            for row in res.itertuples():
                try:
                    obj = Horizons(
                        id=row.Name.strip(),
                        location="500@-95",
                        epochs=row.epoch,
                        id_type="smallbody",
                    )
                    eph = obj.ephemerides(quantities=9)
                except ValueError:
                    obj = Horizons(
                        id=row.Num,
                        location="500@-95",
                        epochs=row.epoch,
                        id_type="smallbody",
                    )
                    eph = obj.ephemerides(quantities=9)
                try:
                    ap_mag[row.Index] = eph["V"].value
                except KeyError:
                    ap_mag[row.Index] = eph["Tmag"].value
            if (ap_mag < 19).any():
                return True

        return False

    def _is_at_edge(self, i_start: int, i_stop: int, window: float = 0.1):
        """
        Check if a candidate is at the edge of a segment of the light curve.

        Parameters
        ----------
        i_start : int
            The start index of the candidate in the light curve.
        i_stop : int
            The stop index of the candidate in the light curve.
        window : float, optional
            The time window (in days) used to check if the candidate is at the edge. Default is 0.1.

        Returns
        -------
        bool
            False if the candidate is not at the edge of a segment of the light curve, True otherwise.
        """

        time = self.time[np.isfinite(self.standardized_flux)].value
        t_start = self.time.value[i_start]
        t_stop = self.time.value[i_stop]

        before = np.nonzero((time > t_start - window) & (time < t_start))[0]
        after = np.nonzero((time > t_stop) & (time < t_stop + window))[0]

        return False if (before.size and after.size) else True

    def query_stellar_parameters(self):
        """
        Query the stellar parameters of the target star.

        This method queries various stellar parameters of the target star, such as parallax,
        Gmag, BP-RP, Tmag, and contamination ratio, from Gaia DR3, TIC, and SIMBAD databases.
        It also checks if the target star has an excluded object type.
        """

        self.stellar_parameters = pd.Series(index=STELLAR_PARAMETER_COLUMNS, dtype=object)

        gaia_dr3_id = query_gaia_dr3_id(self.ticid)
        self.stellar_parameters.gaia_dr3_source_id = gaia_dr3_id
        self.stellar_parameters.obs_duration = np.round(
            self.meta["TIMEDEL"] * np.nonzero(~np.isnan(self.flux.value))[0].size, 4
        )

        # Query parallax, Gmag and BP-RP from Gaia DR3
        if isinstance(gaia_dr3_id, str):
            result = VIZIER.query_constraints("I/355/gaiadr3", Source=gaia_dr3_id)[0]
            plx = result["Plx"].data.data[0]
            if plx > 0:
                self.stellar_parameters["Plx"] = np.round(plx, 4)
            self.stellar_parameters["Gmag"] = np.round(result["Gmag"].data.data[0], 4)
            self.stellar_parameters["BP-RP"] = np.round(result["BP-RP"].data.data[0], 4)

        # Query Tmag and contamination ratio from TIC
        tic_data = Catalogs.query_object(self.label, radius=0.02, catalog="TIC")
        tic_data.add_index("ID")
        try:
            target_row = tic_data.loc[str(self.ticid)]
            self.stellar_parameters.Tmag = target_row["Tmag"]
            self.stellar_parameters.cont_ratio = np.round(target_row["contratio"], 4)
        except KeyError:
            pass

        # Query object info from SIMBAD
        query_result = None
        with warnings.catch_warnings():
            warnings.simplefilter("error", category=UserWarning)
            try:
                query_result = CUSTOM_SIMBAD.query_object(self.label)
            except TableParseError:
                gaia_dr3_id = self.stellar_parameters.gaia_dr3_source_id
                if isinstance(gaia_dr3_id, str):
                    try:
                        query_result = CUSTOM_SIMBAD.query_object(f"Gaia DR3 {gaia_dr3_id}")
                    except TableParseError:
                        pass

        self.meta["exclude"] = False
        if query_result is None:
            self.stellar_parameters.obj_type = np.nan
        else:
            obj_type = query_result["OTYPE"][0]
            self.stellar_parameters.obj_type = obj_type

            if obj_type in EXCLUDED_OTYPES or "CV*" in obj_type.split("|"):
                self.meta["exclude"] = True

    def detrend(self, window_length=0.3):
        """
        Detrend the light curve.

        This method detrends the light curve by masking the eclipses, generating a model,
        and applying a biweight filter to flatten the light curve. The detrended flux is
        stored in a new column, and the standardized flux is calculated.

        Parameters
        ----------
        window_length : float, optional
            The window length (in days) for the detrending process. Default is 0.3.

        This method detrends the light curve by removing systematic trends using a rolling
        window approach. It then standardizes the detrended light curve.
        """

        masked_lc = self._mask_eclipse()
        model_flux = self._generate_model()
        detrended_flux, trend_flux = flatten(
            self.time.value,
            masked_lc.flux - model_flux,
            method="biweight",
            window_length=window_length,
            return_trend=True,
        )
        trend_flux += model_flux
        self.add_columns(
            [detrended_flux * self.flux.unit, trend_flux * self.flux.unit],
            names=["detrended_flux", "trend_flux"],
        )
        self._standardize()

    def find_candidates(self, n_sigma: float = 3, n_consecutive: int = 2):
        """
        Find the candidates of flares.

        This method identifies potential flare candidates in the detrended light curve.
        It searches for outliers above a certain threshold and groups them into
        consecutive events. The method then filters out candidates at the edge of the
        light curve and stores the candidate information in a DataFrame.

        Parameters
        ----------
        n_sigma : float, optional
            The threshold for identifying flare candidates as a multiple of the standard deviation.
            Default is 3.
        n_consecutive : int, optional
            The minimum number of consecutive data points above the threshold to be considered a
            candidate. Default is 2.

        This method identifies potential flare candidates in the standardized light curve using
        the specified threshold and number of consecutive data points.
        """

        self.stellar_parameters.gaia_dr3_source_id = query_gaia_dr3_id(self.ticid)
        self.stellar_parameters.obs_duration = np.round(
            self.meta["TIMEDEL"] * np.nonzero(~np.isnan(self.flux.value))[0].size, 4
        )

        if not self.exclude:
            i_outliers = np.nonzero(self.standardized_flux > n_sigma)[0]

            i_start_array, i_stop_array = find_consecutive(
                i_outliers,
                n_consecutive,
                gap=1.2 * self.meta["TIMEDEL"],
                data=self.time.value,
            )

            if i_start_array is not None:
                i_start_ext_array, i_stop_ext_array = self._extend_multiple_events(i_start_array, i_stop_array)

                at_edge = np.zeros_like(i_start_ext_array, dtype=bool)
                for i in range(at_edge.size):
                    at_edge[i] = self._is_at_edge(i_start_ext_array[i], i_stop_ext_array[i])

                if not at_edge.all():
                    i_start_ext_array = i_start_ext_array[~at_edge]
                    i_stop_ext_array = i_stop_ext_array[~at_edge]

                    i_peak_array = np.copy(i_start_ext_array)
                    for i in range(i_start_ext_array.size):
                        i_peak = self.standardized_flux[i_start_ext_array[i] : i_stop_ext_array[i] + 1].argmax()
                        i_peak_array[i] += i_peak

                    self.candidates = pd.DataFrame(columns=CANDIDATES_COLUMNS)
                    self.candidates.i_start = i_start_ext_array
                    self.candidates.i_peak = i_peak_array
                    self.candidates.i_stop = i_stop_ext_array
                    self.candidates.t_start = np.round(self.time.value[i_start_ext_array], 7)
                    self.candidates.t_peak = np.round(self.time.value[i_peak_array], 7)
                    self.candidates.t_stop = np.round(self.time.value[i_stop_ext_array], 7)

    def detect_sso(self):
        """
        Detect if the candidates are caused by SSO encounters.

        This method checks if the flare candidates identified in the light curve are caused by
        encounters with Solar System Objects (SSOs). It adds a boolean array to the candidates
        DataFrame indicating whether a candidate is caused by an SSO encounter or not.
        """

        if self.candidates is not None:
            sso = np.zeros(len(self.candidates), dtype=bool)
            for row in self.candidates.itertuples():
                sso[row.Index] = self._is_sso(row.i_peak)

            self.candidates.sso = sso

    def calculate_candidate_parameters(self):
        """
        Calculate the parameters of the candidates.

        This method calculates various parameters for the identified flare candidates, such as
        flare probability, signal-to-noise ratio (SNR), amplitude, duration, equivalent duration
        (ED), and energy. The calculated parameters are added to the candidates DataFrame.
        """

        if self.candidates is not None:
            proba_array = np.zeros(len(self.candidates))
            snr_array = np.zeros(len(self.candidates))
            for row in self.candidates.itertuples():
                lc_candidate = self[row.i_start : row.i_stop + 1].remove_nans("standardized_flux")
                time = lc_candidate.time.value
                flux = lc_candidate.standardized_flux.value

                if not (np.diff(lc_candidate.cadenceno) == 1).all():
                    time, flux = fill_gaps(time, flux, lc_candidate.cadenceno)

                if flux.size >= 4:
                    proba_array[row.Index] = round(get_flare_probability(time, flux), 3)
                snr_array[row.Index] = round(np.max(flux), 2)

            self.candidates.flare_prob = proba_array
            self.candidates.snr = snr_array

            if not self.meta["ZERO_CENTERED"]:
                if self.stellar_parameters is None:
                    self.query_stellar_parameters()

                amp = np.zeros(len(self.candidates))
                dur = np.zeros(len(self.candidates))
                ed = np.zeros(len(self.candidates))
                stellar_lum = calculate_stellar_luminosity(self.stellar_parameters.Tmag, self.stellar_parameters.Plx)

                n_row = 0
                for row in self.candidates.itertuples():
                    time = self.time.value[row.i_start : row.i_stop + 1]
                    flux = self.detrended_flux[row.i_start : row.i_stop + 1]
                    amp[n_row] = np.nanmax(flux) - 1
                    dur[n_row] = (time[-1] - time[0]) * 1440
                    mask = np.isnan(flux)
                    ed[n_row] = np.trapz(flux[~mask] - 1, x=time[~mask] * 86400)
                    n_row += 1

                self.candidates.amp = np.round(amp, 3)
                self.candidates.dur = np.round(dur, 1)
                self.candidates.ed = np.round(ed, 2)
                if np.isnan(stellar_lum):
                    self.candidates.energy = np.full(len(self.candidates), np.nan)
                else:
                    energy = ed * stellar_lum
                    self.candidates.energy = [np.format_float_scientific(x, precision=2) for x in energy]

    def find_flares(self):
        """
        Find flares in the light curve.

        This method performs a series of steps to identify flares in the light curve. It queries
        the stellar parameters of the target star, detrends the light curve, finds the flare
        candidates, detects if the candidates are caused by SSO encounters, and calculates the
        candidate parameters. The results are stored in the class attributes.
        """

        self.query_stellar_parameters()
        self.detrend()
        self.find_candidates()
        self.detect_sso()
        self.calculate_candidate_parameters()

    def plot_candidates(self, figure_folder, threshold=0.5):
        """Plot the candidates."""

        if self.candidates is not None:
            t_extend = 30.2 * self.meta["TIMEDEL"]
            finite_mask = np.isfinite(self.standardized_flux)

            self.candidates.loc[self.candidates.sso, "flare_prob"] = -999
            cond_list = [
                self.candidates.flare_prob >= threshold,
                self.candidates.flare_prob == -999,
            ]
            candidate_type_array = np.select(cond_list, ["flare", "sso"], "non-flare")
            color_array = np.select(cond_list, ["tab:red", "tab:orange"], "tab:gray")
            with plt.style.context(lk.MPLSTYLE):
                for row in self.candidates.itertuples():
                    candidate_type = candidate_type_array[row.Index]
                    color = color_array[row.Index]
                    figure_subfolder = figure_folder / candidate_type
                    figure_subfolder.mkdir(exist_ok=True)

                    fig = plt.figure(figsize=(14, 4))

                    ax_label = fig.add_subplot(111)
                    ax_label.spines[["top", "bottom", "left", "right"]].set_visible(False)
                    ax_label.set_xlabel("Time - 2457000 [BTJD days]")
                    ax_label.set_ylabel("Normalized Flux")
                    ax_label.minorticks_off()

                    ax_original_lc = fig.add_subplot(221)
                    self.scatter(ax=ax_original_lc, label="")
                    self.plot(
                        ax=ax_original_lc,
                        column="trend_flux",
                        color="tab:red",
                        label="",
                    )
                    ax_original_lc.set_xlabel("")
                    ax_original_lc.set_ylabel("")
                    ax_original_lc.set_xticklabels([])

                    ax_detrended_lc = fig.add_subplot(223)
                    self.scatter(ax=ax_detrended_lc, column="detrended_flux", label="")
                    ax_detrended_lc.plot(self.time.value, 1 + 3 * self.rolling_std, lw=1, c="tab:gray")

                    for element in self.candidates.itertuples():
                        alpha = 0.8 if row.Index == element.Index else 0.3

                        event_flux = self.detrended_flux[slice(element.i_start, element.i_stop + 1)]
                        extra_fill_region = (np.nanmax(event_flux) - np.nanmin(event_flux)) / 20
                        fill_lower_lim = np.nanmin(event_flux) - extra_fill_region
                        fill_upper_lim = np.nanmax(event_flux) + extra_fill_region

                        ax_detrended_lc.fill_between(
                            [element.t_start - 0.06, element.t_stop + 0.06],
                            fill_lower_lim,
                            fill_upper_lim,
                            facecolor=color_array[element.Index],
                            alpha=alpha,
                        )

                        ax_detrended_lc.annotate(
                            element.Index + 1,
                            (element.t_start - 0.5, fill_upper_lim),
                            c=color_array[element.Index],
                            alpha=alpha,
                        )

                    ax_detrended_lc.set_xlim(*ax_original_lc.get_xlim())
                    ax_detrended_lc.set_xlabel("")
                    ax_detrended_lc.set_ylabel("")

                    ax_event = fig.add_subplot(122)
                    ax_event.axhline(3, c="tab:gray", lw=1)
                    ax_event.axhline(1, c="tab:gray", ls="--", lw=1)
                    if candidate_type == "sso":
                        box_str = f"Cand {row.Index + 1}, {candidate_type}"
                    else:
                        box_str = (
                            f"Cand {row.Index + 1}, {candidate_type}\n"
                            f"flare prob: {row.flare_prob}\n"
                            f"snr: {row.snr}\n"
                            f"amp: {row.amp}\n"
                            f"dur: {row.dur} m\n"
                            f"ed: {row.ed} s\n"
                            f"{row.energy} erg"
                        )
                    at = AnchoredText(
                        box_str,
                        loc="upper right",
                        frameon=True,
                        prop={"multialignment": "right"},
                    )
                    at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
                    ax_event.add_artist(at)

                    i_plot = (
                        (self.time.value >= row.t_start - t_extend)
                        & (self.time.value <= row.t_stop + t_extend)
                        & finite_mask
                    )
                    i_event = np.zeros_like(self.time.value, dtype=bool)
                    i_event[row.i_start : row.i_stop + 1] = True
                    i_event = i_event & finite_mask
                    self[i_plot].plot(
                        ax=ax_event,
                        column="standardized_flux",
                        label="",
                        lw=1,
                        ms=5,
                        marker=".",
                    )
                    self[i_event].plot(
                        ax=ax_event,
                        column="standardized_flux",
                        color=color,
                        label="",
                        lw=1.5,
                        ms=5,
                        marker=".",
                    )

                    ax_event.xaxis.set_major_locator(MaxNLocator(5))
                    ax_event.yaxis.set_major_locator(MaxNLocator(integer=True))
                    ax_event.set_xlim(
                        row.t_start - t_extend + self.meta["TIMEDEL"],
                        row.t_stop + t_extend - self.meta["TIMEDEL"],
                    )
                    if self.standardized_flux[i_plot].min() < -8:
                        ax_event.set_ylim(bottom=-8)
                    ax_event.set_xlabel("")
                    ax_event.set_ylabel("Standardized Flux")
                    ax_event.ticklabel_format(useOffset=False)
                    ax_event.yaxis.set_label_position("right")
                    ax_event.yaxis.tick_right()

                    ax_label.set_yticks(ax_detrended_lc.get_yticks())
                    ax_label.tick_params(
                        colors="w",
                        which="both",
                        top=False,
                        bottom=False,
                        left=False,
                        right=False,
                    )

                    period = "{:.2f}d".format(self.period) if self.period > 0 else "/"
                    title = f"{self.label}, Sector {self.sector}, {self.stellar_parameters.obj_type}, P={period}"

                    plt.suptitle(title, y=0.94, fontsize=15)
                    plt.subplots_adjust(hspace=0.05, wspace=0.012)

                    figure_path = figure_subfolder / "{}-S{}-{}.png".format(
                        self.label.replace(" ", ""), self.sector, round(row.t_peak, 7)
                    )
                    plt.savefig(figure_path, bbox_inches="tight")
                    plt.close()
