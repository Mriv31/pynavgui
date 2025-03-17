import importlib
from . import angles
from . import save_utils
from . import step_detection
from . import display_utils
from . import math_utils
from . import copy_utils
from . import measure_utils
from . import filter_utils

importlib.reload(angles)
importlib.reload(step_detection)
importlib.reload(save_utils)
importlib.reload(display_utils)
importlib.reload(math_utils)
importlib.reload(copy_utils)
importlib.reload(measure_utils)
importlib.reload(filter_utils)

from .angles import remove_phase_jumps
from .angles import phir_phiu_unwrap
from .step_detection import (
    get_steps_kernelcpd,
    get_steps_binseg,
    get_steps_bottomup,
    get_steps_msf,
    show_filtered_transitions_from_peak_file,
)
from .save_utils import save_dataset_as_npy
from .display_utils import set_xarraylinsorted, unset_xarraylinsorted
from .math_utils import divide
from .copy_utils import copy_ds_to_new_plot, copy_visible_ds_to_new_plot
from .measure_utils import variance
from .filter_utils import chi2_filter

angles_dict = {
    "Remove phase jumps": remove_phase_jumps,
    "Unwrap phase": phir_phiu_unwrap,
}

step_detection_dict = {
    "KernelCPD": get_steps_kernelcpd,
    "Binseg": get_steps_binseg,
    "BottomUp": get_steps_bottomup,
    "Moving step fit": get_steps_msf,
    "Show filtered transitions from peak file": show_filtered_transitions_from_peak_file,
}

save_utils_dict = {"Save as .npy": save_dataset_as_npy}

display_utils_dict = {
    "Set xArrayLinSorted": set_xarraylinsorted,
    "Unset xArrayLinSorted": unset_xarraylinsorted,
}

math_utils_dict = {"Divide Y": divide}

copy_utils_dict = {
    "Copy dataset to new plot": copy_ds_to_new_plot,
    "Copy visible range of dataset to new plot": copy_visible_ds_to_new_plot,
}

measure_utils_dict = {"Variance": variance}

filter_utils_dict = {"Chi2 filter": chi2_filter}

active_ds_utils = {
    "Angles": angles_dict,
    "Step detection": step_detection_dict,
    "Save": save_utils_dict,
    "Display": display_utils_dict,
    "Math": math_utils_dict,
    "Copy": copy_utils_dict,
    "Measure": measure_utils_dict,
    "Filter": filter_utils_dict,
}
