# Project Repository : https://github.com/robertapplin/pyqt-autotest
# Authored by Robert Applin, 2022
from typing import List, Tuple

from pyqt_autotest.core.action import Action
from pyqt_autotest.core.auto_test import _AutoTest
from pyqt_autotest.qt.widgets import find_child_widgets, get_widget_from_str

from PyQt5.QtWidgets import QWidget


class RepeatableAutoTest(_AutoTest):
    """
    An auto test class for performing a repeatable sequence of actions on widgets within a user widget.
    """

    def _test_type(self) -> str:
        """Returns a string to represent the type of the test."""
        return "RepeatableAutoTest"

    def _get_number_of_actions(self) -> int:
        """Returns the number of actions for this test."""
        return len(self.options.sequence_of_actions)

    def _get_child_widgets(self) -> List[QWidget]:
        """Returns the child widgets which are required for a run."""
        return find_child_widgets(self.widget, [QWidget])

    def _get_action_name_widget_name_and_widget(
        self, action_number: int, all_widgets: List[QWidget]
    ) -> Tuple[Action, str, QWidget]:
        """Returns the action, and widget to perform an action on."""
        action_name = self.options.sequence_of_actions[action_number]
        widget_name = self.options.sequence_of_widgets[action_number]
        widget = get_widget_from_str(all_widgets, widget_name)
        return action_name, widget_name, widget
