import numpy as np
import numba


@numba.njit(parallel=True, fastmath=True)
def chi2_filter_njit(Y, sigma):
    N = len(Y)
    window_sizes = np.linspace(10, 1000, 10)
    window_sizes = window_sizes.astype(np.int32)
    smoothed_Y = np.zeros(N, dtype=np.float64)
    weighted_sum = np.zeros(N, dtype=np.float64)
    for w_idx in numba.prange(len(window_sizes)):
        w = window_sizes[w_idx]
        for i in range(N - w + 1):  # Sliding window over dataset
            Y_window = Y[i : i + w]
            Y_mean = np.sum(Y_window) / w
            chi2_values = np.sum((Y_window - Y_mean) ** 2) / (w * sigma**2)
            weight = np.exp(-chi2_values)
            smoothed_Y[i : i + w] += Y_mean * weight
            weighted_sum[i : i + w] += weight
    return smoothed_Y / weighted_sum


def chi2_filter(dataset, sigma: float = 5):
    return chi2_filter_njit(dataset.y_data(), sigma)
