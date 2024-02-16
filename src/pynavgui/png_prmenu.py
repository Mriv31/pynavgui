# This Python file uses the following encoding: utf-8
from PyQt6 import QtWidgets, QtGui
from .rds_menu import RDSMenu
from .r_plotmenu import RPlotMenu
from . import PngPlot


class PngPlotRegionMenu(QtWidgets.QMenu):
    # Class of menu to be added in any window which has a PyQtRGraph
    # and a method get_current_PyQtRGraph
    def __init__(self, title, window, png_instance=None):
        self.window = window
        super(PngPlotRegionMenu, self).__init__(title, window)
        # self.aboutToHide.connect(self.clear)
        self.aboutToShow.connect(self.create_graph_menu)
        self.png_instance = png_instance

    def create_graph_menu(self):
        self.clear()

        if (
            self.png_instance is not None
            and self.png_instance.active_plot is not None
            and isinstance(self.png_instance.active_plot, PngPlot)
        ):
            self.addMenu(RDSMenu("Cur. Dataset", self, self.png_instance.active_plot))
            self.addMenu(RPlotMenu("Cur. Plot", self, self.png_instance.active_plot))
        else:
            action = QtGui.QAction("No editable graph selected", self)
            action.setEnabled(False)
            self.addAction(action)
        self.show()
