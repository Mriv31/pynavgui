import numpy as np


def copy_ds_to_new_plot(dataset):
    return np.copy(dataset.y_data()), True


def copy_visible_ds_to_new_plot(dataset):
    x_visible, y_visible = dataset.get_visible_data()
    return np.column_stack((np.copy(x_visible), np.copy(y_visible))), True
