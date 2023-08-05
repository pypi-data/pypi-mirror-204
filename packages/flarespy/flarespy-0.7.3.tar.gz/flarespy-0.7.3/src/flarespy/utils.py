import warnings

import joblib
import numpy as np
import pandas as pd

from . import PACKAGEDIR

MODEL_PATH = PACKAGEDIR / "data" / "model.dat"
with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=UserWarning)
    RFC_MODEL = joblib.load(MODEL_PATH)

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
    "gaia3_source_id",
    "parallax",
    "phot_g_mean_mag",
    "phot_bp_mean_mag",
    "phot_rp_mean_mag",
    "tess_mag",
    "obs_duration",
]


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


def get_flare_probability(time, flux):
    time *= 1440
    time -= time.min()
    feature = extract_features(flux)

    return RFC_MODEL.predict_proba(feature)[0][0]


def extend(time, flux, t_start, t_stop, t_max_extend, n_sigma=1, n_left=1, n_right=1, mode=1):
    indexes_range = np.nonzero((time >= t_start - t_max_extend) & (time <= t_stop + t_max_extend))[0]
    i_start = np.nonzero(time == t_start)[0][0]
    i_stop = np.nonzero(time == t_stop)[0][0]

    # left
    def condition_left(index):
        if mode == 1:
            return (flux[index - n_left : index] > n_sigma).any()
        elif mode == -1:
            return (flux[index - n_left : index] < n_sigma).any()
        else:
            raise ValueError("mode must be 1 or -1")

    while condition_left(i_start) and i_start > indexes_range[0]:
        i_start -= 1
        if i_start < n_left:
            i_start = 0
            break
    i_start = max(0, i_start - 1, indexes_range[0])

    # right
    def condition_right(index):
        if mode == 1:
            return (flux[index + 1 : index + 1 + n_right] > n_sigma).any()
        elif mode == -1:
            return (flux[index + 1 : index + 1 + n_right] < n_sigma).any()
        else:
            raise ValueError("mode must be 1 or -1")

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

    if len(grouped_consecutive_data):
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
