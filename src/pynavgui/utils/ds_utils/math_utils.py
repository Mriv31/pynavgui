import numpy as np


def divide(dataset, num: float = 2):
    return np.copy(dataset.y_data()) / num
