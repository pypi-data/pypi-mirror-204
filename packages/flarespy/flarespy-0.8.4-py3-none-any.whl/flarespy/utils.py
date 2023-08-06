import warnings

import astropy.units as u
import joblib
import numpy as np
import pandas as pd
from astropy.coordinates import SkyCoord
from astropy.time import Time
from astroquery.exceptions import TableParseError
from astroquery.gaia import Gaia
from astroquery.mast import Catalogs
from astroquery.simbad import Simbad
from erfa import ErfaWarning

from . import PACKAGEDIR

MODEL_PATH = PACKAGEDIR / "data" / "model.dat"
with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=UserWarning)
    RFC_MODEL = joblib.load(MODEL_PATH)

CUSTOM_SIMBAD = Simbad()
CUSTOM_SIMBAD.add_votable_fields("ids")

Gaia.MAIN_GAIA_TABLE = "gaiadr3.gaia_source"

CANDIDATES_COLUMNS = [
    "i_start",
    "i_peak",
    "i_stop",
    "t_start",
    "t_peak",
    "t_stop",
    "sso",
    "flare_prob",
    "snr",
    "amp",
    "dur",
    "ed",
    "energy",
]

STELLAR_PARAMETER_COLUMNS = [
    "gaia_dr3_source_id",
    "obj_type",
    "Plx",
    "Gmag",
    "BP-RP",
    "Tmag",
    "cont_ratio",
    "obs_duration",
]

# Zero point TESS flux (from Sullivan 2017)
TESS_FLUX0 = 4.03e-6 * u.erg / u.s / u.cm**2


def extract_features(x):
    abs_energy = np.dot(x, x)
    first_location_of_maximum = np.argmax(x) / len(x)

    abs_x = np.abs(x)
    s = np.sum(abs_x)
    mass_centralized = np.cumsum(abs_x) / s
    mass_center = (np.argmax(mass_centralized >= 0.5) + 1) / len(x)

    kurtosis = pd.Series.kurtosis(pd.Series(x))
    length = len(x)
    maximum = np.max(x)
    root_mean_square = np.sqrt(np.mean(np.square(x)))
    skewness = pd.Series.skew(pd.Series(x))
    standard_deviation = np.std(x)

    return pd.DataFrame(
        {
            "flux__abs_energy": [abs_energy],
            "flux__first_location_of_maximum": [first_location_of_maximum],
            "flux__index_mass_quantile__q_0.5": [mass_center],
            "flux__kurtosis": [kurtosis],
            "flux__length": [length],
            "flux__maximum": [maximum],
            "flux__root_mean_square": [root_mean_square],
            "flux__skewness": [skewness],
            "flux__standard_deviation": [standard_deviation],
        }
    )


def calculate_stellar_luminosity(t_mag, plx):
    if isinstance(t_mag, float) and isinstance(plx, float):
        plx /= 1000
        dist = 1 / plx * u.pc
        flux = 10 ** (-t_mag / 2.5) * TESS_FLUX0
        lum = 4 * np.pi * dist.to(u.cm) ** 2 * flux
        return lum.value
    else:
        return np.nan


def get_flare_probability(time, flux):
    time *= 1440
    time -= time.min()
    feature = extract_features(flux)

    return RFC_MODEL.predict_proba(feature)[0][0]


def extend(time, flux, t_start, t_stop, t_max_extend, n_sigma=1, n_left=1, n_right=1, mode=1):
    indexes_range = np.nonzero((time >= t_start - t_max_extend) & (time <= t_stop + t_max_extend))[0]
    i_start = np.nonzero(time == t_start)[0][0]
    i_stop = np.nonzero(time == t_stop)[0][0]

    def condition_left(index):
        if mode == 1:
            return (flux[index - n_left : index] > n_sigma).any()
        elif mode == -1:
            return (flux[index - n_left : index] < n_sigma).any()
        else:
            raise ValueError("mode must be 1 or -1")

    def condition_right(index):
        if mode == 1:
            return (flux[index + 1 : index + 1 + n_right] > n_sigma).any()
        elif mode == -1:
            return (flux[index + 1 : index + 1 + n_right] < n_sigma).any()
        else:
            raise ValueError("mode must be 1 or -1")

    # Extend left
    while condition_left(i_start) and i_start > indexes_range[0]:
        i_start -= 1
        if i_start < n_left:
            i_start = 0
            break
    i_start = max(0, i_start - 1, indexes_range[0])

    # Extend right
    while condition_right(i_stop) and i_stop < indexes_range[-1]:
        i_stop += 1
        if i_stop + 1 + n_right > time.size:
            i_stop = time.size - 1
            break
    i_stop = min(time.size - 1, i_stop + 1, indexes_range[-1])

    return time[i_start], time[i_stop]


def find_consecutive(indexes, n_consecutive, gap=1, data=None):
    if data is None:
        grouped_data = np.split(indexes, np.nonzero(np.diff(indexes) > gap)[0] + 1)
    else:
        grouped_data = np.split(indexes, np.nonzero(np.diff(data[indexes]) > gap)[0] + 1)

    grouped_consecutive_data = [x for x in grouped_data if x.size >= n_consecutive]

    if grouped_consecutive_data:
        i_start_array = np.array([x[0] for x in grouped_consecutive_data], dtype=int)
        i_stop_array = np.array([x[-1] for x in grouped_consecutive_data], dtype=int)
        return i_start_array, i_stop_array
    else:
        return None, None


def fill_gaps(time, flux, cadenceno):
    """Fill gaps in the data by interpolation."""

    newdata = {}

    dt = time - np.median(np.diff(time)) * cadenceno
    ncad = np.arange(cadenceno[0], cadenceno[-1] + 1, 1)
    in_original = np.in1d(ncad, cadenceno)
    ncad = ncad[~in_original]
    ndt = np.interp(ncad, cadenceno, dt)

    ncad = np.append(ncad, cadenceno)
    ndt = np.append(ndt, dt)
    ncad, ndt = ncad[np.argsort(ncad)], ndt[np.argsort(ncad)]
    ntime = ndt + np.median(np.diff(time)) * ncad
    newdata["cadenceno"] = ncad

    nflux = np.zeros(len(ntime))
    nflux[in_original] = flux
    nflux[~in_original] = np.interp(ntime[~in_original], time, flux)

    return ntime, nflux


def query_gaia_dr3_id(tic_id):
    """Query Gaia DR3 ID from TIC ID."""
    mast_result = Catalogs.query_criteria(catalog="TIC", ID=tic_id)
    gaia2_source_id = mast_result["GAIA"].data.data[0]

    if gaia2_source_id != "":
        query = """
                SELECT dr2_source_id, dr3_source_id
                FROM gaiadr3.dr2_neighbourhood
                WHERE dr2_source_id = {gaia2_source_id}
                """
        cross_result = Gaia.launch_job(query.format(gaia2_source_id=gaia2_source_id)).get_results()
        return str(cross_result["dr3_source_id"][0])
    else:
        with warnings.catch_warnings():
            warnings.simplefilter("error", category=UserWarning)
            try:
                simbad_result = CUSTOM_SIMBAD.query_object(f"TIC{tic_id}")
                id_list = simbad_result["IDS"][0].split("|")
                for i in id_list:
                    if "Gaia DR3" in i:
                        return str(i.split(" ")[-1])
            except TableParseError:
                pass

        ra = mast_result["ra"].data.data[0] * u.deg
        dec = mast_result["dec"].data.data[0] * u.deg
        pm_ra = mast_result["pmRA"].data.data[0] * u.mas / u.yr
        pm_dec = mast_result["pmDEC"].data.data[0] * u.mas / u.yr
        if ~np.isnan(pm_ra) and ~np.isnan(pm_dec):
            coords_j2000 = SkyCoord(ra, dec, pm_ra_cosdec=pm_ra, pm_dec=pm_dec, frame="icrs", obstime=Time("J2000"))
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=ErfaWarning)
                coords = coords_j2000.apply_space_motion(new_obstime=Time("J2016"))
        else:
            coords = SkyCoord(ra, dec, frame="icrs")
        radius = u.Quantity(1, u.arcmin)
        gaia_result = Gaia.cone_search_async(coords, radius, columns=["source_id"]).get_results()
        if (gaia_result["dist"] < (3 / 3600)).any():
            return str(gaia_result["source_id"].data.data[0])

    return np.nan
