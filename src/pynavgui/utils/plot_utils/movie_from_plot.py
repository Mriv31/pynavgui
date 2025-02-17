from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...png_plot import PngPlot
import os
import numpy as np
from PyQt6.QtWidgets import QInputDialog, QFileDialog, QMessageBox, QProgressDialog
from PyQt6.QtCore import Qt
import pyqtgraph.exporters as pg_exporters


def create_movie_from_plot(
    plot: "PngPlot",
):

    ds = plot.get_active_dataset()
    if ds is None:
        QMessageBox.critical(None, "Error", "No active dataset found.")
        return

    window, ok = QInputDialog.getDouble(
        None,
        "Input Duration",
        "Enter duration:",
        0.01,
        0.00001,
        10000.0,
        6,
    )
    if not ok:
        return
  

    overlap, ok = QInputDialog.getDouble(
        None,
        "Input Overlap",
        "Enter Overlap:",
        window / 10,
        window / 100,
        window,
        6,
    )
    if not ok:
        return

    x_min = ds.get_x_min()
    x_max = ds.get_x_max()

    if x_min is None or x_max is None:
        return

    if ds.parentplot is None:
        return

    x_min, ok = QInputDialog.getDouble(
        None,
        "Input Start",
        "Enter Start:",
        x_min,
        x_min,
        x_max,
        6,
    )
    if not ok:
        return
    x_max, ok = QInputDialog.getDouble(
        None,
        "Input Stop",
        "Enter Stop:",
        x_max,
        x_min,
        x_max,
        6,
    )
    if not ok:
        return
    
      use_constant_yspan, ok = QInputDialog.getItem(
        None,
        "Y Span Option",
        "Use constant Y span?",
        ["Yes", "No"],
        0,
        False,
    )
    if not ok:
        return

    ymin = ds.get_y_min()
    ymax = ds.get_y_max()
    yspan = None
    if use_constant_yspan == "Yes":
        yspan, ok = QInputDialog.getDouble(
            None,
            "Input Y span",
            "Enter Y span:",
            ymax - ymin,
            0,
            ymax - ymin,
            6,
        )
    if not ok:
        return

    output_folder = QFileDialog.getExistingDirectory(None, "Select Output Folder", None)
    if not output_folder:
        return
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    window_list = []

    for i in np.arange(x_min, x_max, overlap):
        window_list.append((i, i + window))
    progress = QProgressDialog("Generating frames...", "Cancel", 0, len(window_list))
    progress.setWindowTitle("Progress")
    progress.setWindowModality(Qt.WindowModality.WindowModal)
    progress.setMinimumDuration(0)

    # Block UI updates globally (except QProgressDialog)
    plot.setUpdatesEnabled(False)  # Prevents UI updates for the plot

    for i, win in enumerate(window_list):
        if progress.wasCanceled():
            break

        progress.setValue(i)

        plot.setXRange(win[0], win[1])
        plot.plotItem.vb.autoRangeY(
            yspan=yspan
        )  # This would normally trigger a UI update
        exporter = pg_exporters.ImageExporter(plot.plotItem)
        exporter.parameters()["width"] = 1920
        exporter.export(f"{output_folder}/{i}.png")

    # Re-enable UI updates after loop
    plot.setUpdatesEnabled(True)

    progress.setValue(len(window_list))
