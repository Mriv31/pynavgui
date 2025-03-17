# This Python file uses the following encoding: utf-8
from PyQt6 import QtWidgets, QtGui
import importlib
from .ds_style_menu import dsStyleMenu
from .input_f import InputF
from .utils import ds_utils
from .utils.func_utils.menu_func import add_dict_to_menu


class RDSMenu(QtWidgets.QMenu):

    def __init__(self, title, parent, plot):
        super(RDSMenu, self).__init__(title, parent)
        PDs = plot.get_active_dataset()
        importlib.reload(ds_utils)
        active_ds_utils = ds_utils.active_ds_utils
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
        add_dict_to_menu(utils_menu, active_ds_utils, PDs=PDs)
        self.addMenu(utils_menu)

    def set_ds_name(self):
        (s,) = InputF(
            "Current dataset name is "
            + str(self.PDs.prop["name"])
            + ".\n Please enter new name %s"
        )
        if s is not None:
            self.PDs.change_name(s)
