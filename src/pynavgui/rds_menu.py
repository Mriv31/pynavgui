# This Python file uses the following encoding: utf-8
from PyQt6 import QtWidgets, QtGui
from .ds_style_menu import dsStyleMenu
from .input_f import InputF
from .utils.ds_utils import active_ds_utils


class RDSMenu(QtWidgets.QMenu):
    def __init__(self, title, parent, plot):
        super(RDSMenu, self).__init__(title, parent)
        PDs = plot.get_active_dataset()

        if PDs is None:
            action = QtGui.QAction("No dataset selected", self)
            self.addAction(action)
            action.setDisabled(True)
            return
        self.PDs = PDs
        nameaction = QtGui.QAction("Set dataset name", self)
        nameaction.triggered.connect(self.set_ds_name)
        self.addAction(nameaction)
        self.addMenu(dsStyleMenu("Style", parent=self, PDs=PDs))

        utils_menu = QtWidgets.QMenu("Utils", self)
        for util_name, util_func in active_ds_utils.items():
            action = QtGui.QAction(util_name, self)
            action.triggered.connect(lambda _, func=util_func: func(PDs))
            utils_menu.addAction(action)
        self.addMenu(utils_menu)

    def set_ds_name(self):
        (s,) = InputF(
            "Current dataset name is "
            + str(self.PDs.prop["name"])
            + ".\n Please enter new name %s"
        )
        if s is not None:
            self.PDs.change_name(s)
