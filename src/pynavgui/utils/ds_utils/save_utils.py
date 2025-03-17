import numpy as np


def save_dataset_as_npy(dataset, output_file_npy: str = None):
    if output_file_npy is None:
        return
        # if only_y:
        #     filename = file.absoluteFilePath()
        #     np.save(filename, dataset.y_data())
        # else:
    np.save(output_file_npy, np.vstack((dataset.x_data(), dataset.y_data())))
