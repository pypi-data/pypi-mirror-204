# Project Repository : https://github.com/robertapplin/pyqt-autotest
# Authored by Robert Applin, 2022
from typing import List

from pyqt_autotest.results.exit_state import ExitState
from pyqt_autotest.results.json_results_dict import JSONResultsDict
from pyqt_autotest.qt.top_level_widgets import clear_top_level_widgets, get_top_level_widget_list_as_str
from pyqt_autotest.utilities.print_colors import PrintColors

"""
Errors that occur due to invalid data or an setup being passed into pyqt-autotest.
"""


class SetupError(Exception):
    base_message: str = "\tAn invalid widget setup has been detected, please correct the following:\n\n    "
    class_message: str = ""

    def report(self):
        messages = [f"{PrintColors.ERROR}", self.base_message, self.class_message, f"{PrintColors.END}"]
        print("".join(messages))
        JSONResultsDict().save_run_result(ExitState.Error, messages)


class ActionDoesNotExist(SetupError):
    class_message: str = "\t\tAn action provided in the RepeatableAutoTest does not exist."


class WidgetDoesNotExist(SetupError):
    class_message: str = "\t\tA widget provided in the RepeatableAutoTest does not exist."


class WidgetNotProvidedError(SetupError):
    class_message: str = "\t\tThe provided user class does not implement a 'self.widget' member which is a QWidget."


class NoEnabledChildrenWidgetsError(SetupError):
    class_message: str = "\t\tThe provided widget does not contain any children widgets which are enabled."


"""
Common errors that are found within a widget.
"""


class WidgetError(Exception):
    class_message: str = ""

    def report(self, messages: List[str]):
        print("".join(messages))

    def cleanup(self):
        pass


class CloseWidgetError(WidgetError):
    class_message: str = "Unexpected top level widget(s) detected after closing your widget:\n\n"

    def report(self):
        messages = [
            f"\t{PrintColors.WARNING}",
            self.class_message,
            f"\t\t{get_top_level_widget_list_as_str()}\n{PrintColors.END}",
        ]
        JSONResultsDict().save_run_result(ExitState.Warning, messages)
        super().report(messages)

    def cleanup(self):
        clear_top_level_widgets()
