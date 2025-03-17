# This Python file uses the following encoding: utf-8
from PyQt6 import QtWidgets, QtGui
import importlib
from .action_style import MenuStyler
from .utils import plot_utils


class DsSelectMenu(QtWidgets.QMenu):
    def __init__(self, title, parent, plot):
        super(DsSelectMenu, self).__init__(title, parent)
        for ds in plot.dsl:
            action = QtGui.QAction(ds.prop["name"], self)
            action.triggered.connect(lambda _, y=ds: plot.set_active_dataset(y))
            self.addAction(action)
        styler = MenuStyler(self)

        for ds in plot.dsl:
            if ds.prop["pen"] is not None:
                styler.setColor(ds.prop["name"], ds.prop["pen"])
            elif ds.prop["symbolPen"] is not None:
                styler.setColor(ds.prop["name"], ds.prop["symbolPen"])
            else:
                styler.setColor(ds.prop["name"], "k")


class RPlotMenu(QtWidgets.QMenu):
    def __init__(self, title, parent, plot):
        super(RPlotMenu, self).__init__(title, parent)
        importlib.reload(plot_utils)
        remove_active_plot = QtGui.QAction("Remove active plot", self)
        remove_active_plot.triggered.connect(plot.del_from_graph)

        remove_active_dataset = QtGui.QAction("Remove active dataset", self)
        remove_active_dataset.triggered.connect(plot.remove_active_dataset)

        self.addAction(remove_active_plot)
        self.addAction(remove_active_dataset)

        self.addMenu(DsSelectMenu("Select active data set", self, plot))
        utils_menu = QtWidgets.QMenu("Utils", self)
        active_plot_utils = plot_utils.active_plot_utils
        for util_name, util_func in active_plot_utils.items():
            action = QtGui.QAction(util_name, self)
            action.triggered.connect(lambda _, func=util_func: func(plot))
            utils_menu.addAction(action)
        self.addMenu(utils_menu)
