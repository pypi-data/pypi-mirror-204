# Project Repository : https://github.com/robertapplin/pyqt-autotest
# Authored by Robert Applin, 2022
from typing import List, Tuple

from pyqt_autotest.core.action import Action
from pyqt_autotest.core.auto_test import _AutoTest
from pyqt_autotest.qt.widgets import find_child_widgets, get_widget_name
from pyqt_autotest.utilities.randomizer import get_random_action, get_random_widget

from PyQt5.QtWidgets import QWidget


class RandomAutoTest(_AutoTest):
    """
    An auto test class for performing random actions on random widgets within a user widget.
    """

    def _test_type(self) -> str:
        """Returns a string to represent the type of the test."""
        return "RandomAutoTest"

    def _get_number_of_actions(self) -> int:
        """Returns the number of actions for this test."""
        return self.options.number_of_actions

    def _get_child_widgets(self) -> List[QWidget]:
        """Returns the child widgets which are required for a run."""
        return find_child_widgets(self.widget, list(self.options.widget_actions.keys()))

    def _get_action_name_widget_name_and_widget(self, _, all_widgets: List[QWidget]) -> Tuple[Action, str, QWidget]:
        """Returns the action, and widget to perform an action on."""
        widget = get_random_widget(all_widgets)
        widget_name = get_widget_name(widget)
        action_name = get_random_action(type(widget), self.options.widget_actions)
        return action_name, widget_name, widget
