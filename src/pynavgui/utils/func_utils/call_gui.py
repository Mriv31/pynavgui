import inspect
import numpy as np
from PyQt6.QtWidgets import QInputDialog
from PyQt6.QtWidgets import QFileDialog


def get_function_args(func):
    sig = inspect.signature(func)
    args = {}
    for name, param in sig.parameters.items():
        if param.default is param.empty:
            args[name] = (param.annotation, None)
        else:
            args[name] = (param.annotation, param.default)
    return args


def call_function_with_user_input(func, data_set_or_plot):
    # only for ds so far
    args = get_function_args(func)
    first_arg_name = next(iter(args))
    args.pop(first_arg_name)
    # Check the class name of data_set_or_plot

    kwargs = {}
    for name, (arg_type, default) in args.items():
        if arg_type == float:
            value, ok = QInputDialog.getDouble(
                None,
                f"Enter value for {name}",
                f"Default: {default}",
                default,
                decimals=6,
            )
            if ok:
                kwargs[name] = value
            else:
                return
        elif arg_type == int:
            value, ok = QInputDialog.getInt(
                None, f"Enter value for {name}", f"Default: {default}", default
            )
            if ok:
                kwargs[name] = value
            else:
                return
        elif arg_type == bool:
            value, ok = QInputDialog.getItem(
                None,
                f"Enter value for {name}",
                f"Default: {default}",
                ["True", "False"],
                0,
                False,
            )
            if ok:
                kwargs[name] = value == "True"
            else:
                return
        elif name == "output_file_npy":
            value = QFileDialog.getSaveFileName(
                None, f"Select file for {name}, or cancel", "", "Npy files (*.npy)"
            )
            if value == ("", ""):
                return
            kwargs[name] = value[0]

        elif name == "output_file_npz":
            value = QFileDialog.getSaveFileName(
                None, f"Select file for {name}, or cancel", "", "Npz files (*.npz)"
            )
            if value == ("", ""):
                return
            kwargs[name] = value[0]

        elif name == "input_file_npy":
            value = QFileDialog.getOpenFileName(
                None, f"Select file for {name}, or cancel", "", "Npy files (*.npy)"
            )
            if value == ("", ""):
                return
            kwargs[name] = value[0]

        elif name == "input_file_npz":
            value = QFileDialog.getOpenFileName(
                None, f"Select file for {name}, or cancel", "", "Npz files (*.npz)"
            )
            if value == ("", ""):
                return
            kwargs[name] = value[0]

        else:
            value, ok = QInputDialog.getText(
                None, f"Enter value for {name}", f"Default: {default}", str(default)
            )
            if ok:
                kwargs[name] = value
            else:
                return

    res = func(data_set_or_plot, **kwargs)
    new_plot = False
    if isinstance(res, np.ndarray):
        data = res
    elif isinstance(res, tuple):
        if len(res) == 2:
            data, new_plot = res
        else:
            return
    else:
        return

    if not new_plot:
        if data.ndim == 1:
            data_set_or_plot.parentplot.add_ds(
                np.copy(data_set_or_plot.x_data()),
                data,
                like=data_set_or_plot,
                name=f"{data_set_or_plot.prop['name']} {func.__name__}",
            )
        elif data.ndim == 2:
            data_set_or_plot.parentplot.add_ds(
                data[:, 0],
                data[:, 1],
                name=f"{data_set_or_plot.prop['name']} {func.__name__}",
            )
    else:
        if data.ndim == 1:
            data_set_or_plot.parentplot.parentplotregion.add_plot(
                x=np.copy(data_set_or_plot.x_data()),
                y=data,
                like=data_set_or_plot,
                name=f"{data_set_or_plot.prop['name']} {func.__name__}",
            )
        elif data.ndim == 2:
            data_set_or_plot.parentplot.parentplotregion.add_plot(
                x=data[:, 0],
                y=data[:, 1],
                name=f"{data_set_or_plot.prop['name']} {func.__name__}",
            )
