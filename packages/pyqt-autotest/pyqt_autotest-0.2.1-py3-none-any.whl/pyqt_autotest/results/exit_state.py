# Project Repository : https://github.com/robertapplin/pyqt-autotest
# Authored by Robert Applin, 2022
from enum import Enum


class ExitState(str, Enum):
    """
    An enum that is used to specify the outcome of testing a widget.
    """

    Success = "Success"
    Warning = "Warning"
    Error = "Error"
