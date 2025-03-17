import numpy as np


def remove_phase_jumps(
    dataset,
    threshold: float = 45,
    shift: int = 10,
    window: int = 1000,
) -> np.ndarray:
    """
    Remove phase jumps in an array of angles.
    """
    data = np.copy(dataset.y_data())
    diff = np.diff(data)
    jumps = np.where(np.abs(diff) > threshold)[0]
    for jump in jumps:
        if jump - shift - window < 0 or jump + shift + window > len(data):
            continue
        b_left = np.mean(data[jump - shift - window : jump - shift])
        b_right = np.mean(data[jump + shift : jump + shift + window])

        i = 0
        while b_right - b_left < -90:
            i += 1
            b_right += 180
        while b_right - b_left > 90:
            i -= 1
            b_right -= 180
        data[jump:] += i * 90

    return data


def phir_phiu_unwrap(dataset, threshold: float = 30, window: int = 1000) -> np.ndarray:
    data_ori = dataset.y_data()
    data = np.copy(data_ori)
    diff = np.diff(data)
    jumps = np.where(np.abs(diff) > threshold)[0]
    naninds = []
    for jump in jumps:
        data[jump - window // 2 : jump + window // 2] = np.nan
        naninds.append((jump - window // 2, jump + window // 2))

    data[~np.isnan(data)] = np.unwrap(data[~np.isnan(data)] % 180, period=180)
    for ind in naninds:
        nan_segment = data_ori[ind[0] : ind[1]]
        average = np.mean(nan_segment)
        i = 0
        while average - data[ind[1] + window // 2] > 90:
            average -= 180
            i -= 1
        while average - data[ind[1] + window // 2] < -90:
            average += 180
            i += 1
        data[ind[0] : ind[1]] = data_ori[ind[0] : ind[1]] + i * 180
    return data
