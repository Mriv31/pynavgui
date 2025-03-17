import ruptures as rpt
import numpy as np
from numba import njit
from scipy.signal import find_peaks
from scipy.ndimage import gaussian_filter1d


@njit
def moving_step_fit(signal, w: int = 100, ts: float = 5, tMSF: float = 0.1):
    """Detects steps in a signal using the Moving Step Fit (MSF) algorithm."""
    n = len(signal)
    stepsize = np.zeros(n)
    step_scores = np.zeros(n)
    print(tMSF)

    for i in range(w // 2, n - w // 2):
        mi_left = np.mean(signal[i - w // 2 : i])
        mi_right = np.mean(signal[i : i + w // 2])
        mi = np.mean(signal[i - w // 2 : i + w // 2])

        RSS_left = np.sum((signal[i - w // 2 : i] - mi_left) ** 2)
        RSS_right = np.sum((signal[i : i + w // 2] - mi_right) ** 2)
        RSS = np.sum((signal[i - w // 2 : i + w // 2] - mi) ** 2)

        MFS_i = abs(mi_right - mi_left) * abs(RSS - RSS_right - RSS_left)

        step_scores[i] = MFS_i
        stepsize[i] = abs(mi_right - mi_left)

    return step_scores, stepsize


def get_steps_msf(
    dataset,
    w: int = 100,
    ts: float = 5,
    tMSF: float = 1000,
    output_file_npz: str = None,
):
    ar = dataset.y_data()
    score, steps = moving_step_fit(ar, w=w, ts=ts, tMSF=tMSF)
    score = gaussian_filter1d(score, sigma=w // 4)
    peaks, _ = find_peaks(score, height=tMSF, prominence=tMSF / 2)
    peaks = peaks[steps[peaks] > ts]
    while True:
        m = np.array([np.mean(a) for a in np.hsplit(ar, peaks)])
        too_small = np.where(np.abs(np.diff(m)) < 0.8 * ts)[0]

        print(too_small)
        if len(too_small) == 0:
            break
        peaks = np.delete(peaks, too_small)
    res = np.zeros_like(ar)
    peaks = np.insert(peaks, 0, 0)
    peaks = np.insert(peaks, len(peaks), len(ar))
    for i in range(len(peaks) - 1):
        res[peaks[i] : peaks[i + 1]] = m[i]
    if output_file_npz is not None:
        np.savez(output_file_npz, peaks=peaks, m=m)
    return res


def filtered_transitions_from_peaks(peaks, m, ar):
    res = np.zeros_like(ar)
    for i in range(len(peaks) - 1):
        res[peaks[i] : peaks[i + 1]] = m[i]
    return res


def show_filtered_transitions_from_peak_file(dataset, input_file_npz):
    trans = np.load(input_file_npz)
    peaks = trans["peaks"]
    m = trans["m"]
    ar = dataset.y_data()
    res = filtered_transitions_from_peaks(peaks, m, ar)
    return res


def get_steps_kernelcpd(dataset, min_size: int = 10, penalty_value: float = 20):
    ar = dataset.y_data()
    algo_c = rpt.KernelCPD(kernel="linear", min_size=min_size).fit(ar)  # "rbf"
    result = algo_c.predict(pen=penalty_value)
    m = [np.mean(a) for a in np.hsplit(ar, result)]
    res = np.zeros_like(ar)
    result = np.insert(result, 0, 0)
    result = np.insert(result, len(result), len(ar))
    for i in range(len(result) - 1):
        res[result[i] : result[i + 1]] = m[i]
    print(res.ndim)
    return res


def get_steps_binseg(dataset, sigma: float = 5, jump: int = 10):
    model = "l2"
    ar = dataset.y_data()
    n = len(ar)
    algo = rpt.Binseg(model=model, jump=jump).fit(ar)
    result = algo.predict(epsilon=3 * n * sigma**2)

    m = [np.mean(a) for a in np.hsplit(ar, result)]
    res = np.zeros_like(ar)
    result = np.insert(result, 0, 0)
    result = np.insert(result, len(result), len(ar))
    for i in range(len(result) - 1):
        res[result[i] : result[i + 1]] = m[i]
    print(res.ndim)
    return res


def get_steps_bottomup(dataset, sigma: float = 5, jump: int = 10):
    ar = dataset.y_data()
    n = len(ar)
    model = "l2"
    algo = rpt.BottomUp(model=model, jump=jump).fit(ar)
    result = algo.predict(epsilon=3 * n * sigma**2)

    m = [np.mean(a) for a in np.hsplit(ar, result)]
    res = np.zeros_like(ar)
    result = np.insert(result, 0, 0)
    result = np.insert(result, len(result), len(ar))
    for i in range(len(result) - 1):
        res[result[i] : result[i + 1]] = m[i]
    print(res.ndim)
    return res
