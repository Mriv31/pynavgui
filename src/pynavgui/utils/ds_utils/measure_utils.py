from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt
import numpy as np


def variance(dataset):
    msg_box = QMessageBox()
    if QApplication.keyboardModifiers() & Qt.KeyboardModifier.ShiftModifier:
        xd, yd = dataset.get_visible_data()
        xmin, xmax = np.min(xd), np.max(xd)
        var = np.var(yd)
        msg_box.setText(f"The variance between x = {xmin} and x = {xmax} is : {var}")
    else:
        var = np.var(dataset.y_data())
        msg_box.setText(f"The variance of the whole dataset is : {var}")

    msg_box.exec()
