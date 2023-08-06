# Project Repository : https://github.com/robertapplin/pyqt-autotest
# Authored by Robert Applin, 2022
from typing import Callable, Dict, List

from pyqt_autotest.core.action import Action

from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QPushButton

DEFAULT_NUMBER_OF_RUNS = 1
DEFAULT_NUMBER_OF_ACTIONS = 10
DEFAULT_SEQUENCE_OF_ACTIONS = []
DEFAULT_SEQUENCE_OF_WIDGETS = []
DEFAULT_WAIT_TIME = 50
DEFAULT_VERBOSE = False


class Options:
    actions: Dict[Action, Callable] = {
        Action.KeyDownClick: lambda widget: QTest.keyClick(widget, Qt.Key_Down),
        Action.KeyUpClick: lambda widget: QTest.keyClick(widget, Qt.Key_Up),
        Action.MouseLeftClick: lambda widget: QTest.mouseClick(widget, Qt.LeftButton),
    }

    widget_actions = {QPushButton: [Action.MouseLeftClick]}

    def __init__(
        self, number_of_runs: int = None, number_of_actions: int = None, wait_time: int = None, verbose: bool = False
    ):
        self._number_of_runs: int = number_of_runs
        self._wait_time: int = wait_time
        self._verbose: bool = verbose

        # Options only used for RandomAutoTest
        self._number_of_actions: int = number_of_actions

        # Options only used for RepeatableAutoTest
        self._sequence_of_actions: List[Action] = None
        self._sequence_of_widgets: List[str] = None

    @property
    def number_of_runs(self) -> int:
        """Returns the number_of_runs option, or a default if it hasn't been set."""
        if self._number_of_runs is None:
            return DEFAULT_NUMBER_OF_RUNS
        return int(self._number_of_runs)

    @number_of_runs.setter
    def number_of_runs(self, n_runs: int) -> None:
        """Sets the number_of_runs option if it hasn't already been provided on the command line."""
        if n_runs is None:
            return
        if not isinstance(n_runs, int):
            raise ValueError("The provided 'number_of_runs' option is not an int.")

        if self._number_of_runs is None:
            self._number_of_runs = n_runs

    @property
    def number_of_actions(self) -> int:
        """Returns the number_of_actions option, or a default if it hasn't been set."""
        if self._number_of_actions is None:
            return DEFAULT_NUMBER_OF_ACTIONS
        return int(self._number_of_actions)

    @number_of_actions.setter
    def number_of_actions(self, n_actions: int) -> None:
        """Sets the number_of_actions option if it hasn't already been provided on the command line."""
        if n_actions is None:
            return
        if not isinstance(n_actions, int):
            raise ValueError("The provided 'number_of_actions' option is not an int.")

        if self._number_of_actions is None:
            self._number_of_actions = n_actions

    @property
    def wait_time(self) -> int:
        """Returns the wait_time option, or a default if it hasn't been set."""
        if self._wait_time is None:
            return DEFAULT_WAIT_TIME
        return int(self._wait_time)

    @wait_time.setter
    def wait_time(self, wait_time: int) -> None:
        """Sets the wait_time option if it hasn't already been provided on the command line."""
        if wait_time is None:
            return
        if not isinstance(wait_time, int):
            raise ValueError("The provided 'wait_time' option is not an int.")

        if self._wait_time is None:
            self._wait_time = wait_time

    @property
    def sequence_of_actions(self) -> List[Action]:
        """Returns the sequence_of_actions option, or a default if it hasn't been set."""
        if self._sequence_of_actions is None:
            return DEFAULT_SEQUENCE_OF_ACTIONS
        return self._sequence_of_actions

    @sequence_of_actions.setter
    def sequence_of_actions(self, actions: List[Action]) -> None:
        """Sets the sequence_of_actions option if it hasn't already been provided on the command line."""
        if actions is None:
            return
        if not isinstance(actions, list):
            raise ValueError("The provided 'sequence_of_actions' option is not a list.")

        if self._sequence_of_actions is None:
            self._sequence_of_actions = [action.strip() for action in actions]

    @property
    def sequence_of_widgets(self) -> List[str]:
        """Returns the sequence_of_widgets option, or a default if it hasn't been set."""
        if self._sequence_of_widgets is None:
            return DEFAULT_SEQUENCE_OF_WIDGETS
        return self._sequence_of_widgets

    @sequence_of_widgets.setter
    def sequence_of_widgets(self, widgets: List[str]) -> None:
        """Sets the sequence_of_widgets option if it hasn't already been provided on the command line."""
        if widgets is None:
            return
        if not isinstance(widgets, list):
            raise ValueError("The provided 'sequence_of_widgets' option is not a list.")

        if self._sequence_of_widgets is None:
            self._sequence_of_widgets = [widget.strip() for widget in widgets]

    @property
    def verbose(self) -> bool:
        """Returns the verbose option, or a default if it hasn't been set."""
        if self._verbose is None:
            return DEFAULT_VERBOSE
        return bool(self._verbose)

    @verbose.setter
    def verbose(self, verbose: bool) -> None:
        """Sets the verbose option if it hasn't already been provided on the command line."""
        if verbose is None:
            return
        if not isinstance(verbose, bool):
            raise ValueError("The provided 'verbose' option is not a boolean.")

        if self._verbose is None:
            self._verbose = verbose
