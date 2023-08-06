# Project Repository : https://github.com/robertapplin/pyqt-autotest
# Authored by Robert Applin, 2022
import sys
from abc import ABCMeta, abstractmethod
from inspect import getsource
from typing import List, Tuple

from pyqt_autotest.cli.options import Options
from pyqt_autotest.core.action import Action
from pyqt_autotest.core.exception_handler import catch_exceptions, exception_hook, exit_hook, unraisable_exception_hook
from pyqt_autotest.core.exceptions import ActionDoesNotExist, CloseWidgetError, WidgetDoesNotExist, WidgetNotProvidedError
from pyqt_autotest.results.exit_state import ExitState
from pyqt_autotest.results.json_results_dict import JSONResultsDict
from pyqt_autotest.qt.modal_unblocker import close_modals_if_exist, WindowUnblockFilter
from pyqt_autotest.qt.top_level_widgets import get_top_level_widget_classes
from pyqt_autotest.utilities.print_colors import PrintColors
from pyqt_autotest.utilities.verbosity_controller import VerbosityController

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtTest import QTest
from tqdm import tqdm


class _AutoTest(metaclass=ABCMeta):
    def __init__(self, options: Options, verbosity_controller: VerbosityController):
        super(_AutoTest, self).__init__()
        self.widget: QWidget = None
        self.options: Options = options

        self._verbosity_controller = verbosity_controller
        self._logger = JSONResultsDict()

        # Used to unblock the main widget if a modal QFileDialog opens and blocks further actions
        self.modal_unblocker = WindowUnblockFilter()

        sys.exit = exit_hook
        sys.excepthook = exception_hook
        sys.unraisablehook = unraisable_exception_hook

    def setup_options(self) -> None:
        """The method used to set the options for the test (optional)."""
        pass

    @abstractmethod
    def setup_widget(self) -> None:
        """The method used to instantiate the users widget."""
        pass

    @catch_exceptions
    def _run(self, test_name: str, import_str: str) -> None:
        """Runs the random widget testing."""
        self.setup_options()
        self._logger.init_test(self._test_type(), import_str, getsource(self.setup_widget), test_name, self.options)
        for run_number in range(1, self.options.number_of_runs + 1):
            self._logger.init_run()
            self._run_actions(run_number)

    @catch_exceptions
    def _run_actions(self, run_number: int) -> None:
        """Sets up the widget and runs the actions for a single run."""
        self.setup_widget()
        if not isinstance(self.widget, QWidget):
            raise WidgetNotProvidedError()
        self.widget.setAttribute(Qt.WA_DeleteOnClose)
        self.widget.installEventFilter(self.modal_unblocker)
        self.widget.show()

        child_widgets = self._get_child_widgets()
        with self._verbosity_controller:
            print(
                f"\t{PrintColors.INFO}Starting test number "
                f"({run_number}/{self.options.number_of_runs})...{PrintColors.END}\n"
            )
            for action_number in tqdm(
                range(self._get_number_of_actions()),
                desc=f"\tRunning ({run_number}/{self.options.number_of_runs})",
                disable=self.options.verbose,
                bar_format="{l_bar}{bar}|",
                ncols=80,
            ):
                # After a certain timeout, attempt to close any QMessageBox's that could be blocking the main widget
                QTimer.singleShot(2 * self.options.wait_time, lambda: close_modals_if_exist(QMessageBox))
                action_name, widget_name, widget = self._get_action_name_widget_name_and_widget(action_number, child_widgets)
                self._logger.save_event(widget_name, str(action_name))
                # Validate the widget and action exists
                if widget is None:
                    raise WidgetDoesNotExist()
                if action_name not in self.options.actions:
                    raise ActionDoesNotExist()
                # Perform action on a child widget
                self.options.actions[action_name](widget)
                # Wait for a given number of milliseconds
                QTest.qWait(self.options.wait_time)
                # If there was an error which has been caught
                if not self._logger.is_running():
                    break
        self._close_widget()

    @abstractmethod
    def _test_type(self) -> str:
        """Returns a string to represent the type of the test. e.g. RandomAutoTest or RepeatableAutoTest."""
        pass

    @abstractmethod
    def _get_number_of_actions(self) -> int:
        """Returns the number of actions to be performed for a run."""
        pass

    @abstractmethod
    def _get_child_widgets(self) -> List[QWidget]:
        """Returns the child widgets which are required for a run."""
        pass

    @abstractmethod
    def _get_action_name_widget_name_and_widget(
        self, action_number: int, all_widgets: List[QWidget]
    ) -> Tuple[Action, str, QWidget]:
        """Returns the action, and widget to perform an action on."""
        pass

    @catch_exceptions
    def _close_widget(self) -> None:
        """Closes the widget and starts the event loop to ensure all events are processed."""
        self.widget.close()
        self.widget = None
        QTest.qWait(self.options.wait_time)

        if self._logger.is_running():
            if len(get_top_level_widget_classes()) == 0:
                self._logger.save_run_result(ExitState.Success)
            else:
                raise CloseWidgetError()
