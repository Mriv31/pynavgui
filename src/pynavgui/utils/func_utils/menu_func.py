from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QAction
from .call_gui import call_function_with_user_input


def add_dict_to_menu(menu, dictionnary, PDs=None):
    for name, func in dictionnary.items():
        if isinstance(func, dict):
            sub_menu = QMenu(name, menu)
            add_dict_to_menu(sub_menu, func, PDs=PDs)
            menu.addMenu(sub_menu)
        else:
            action = QAction(name, menu)
            action.triggered.connect(
                lambda _, func=func: call_function_with_user_input(func, PDs)
            )
            menu.addAction(action)
