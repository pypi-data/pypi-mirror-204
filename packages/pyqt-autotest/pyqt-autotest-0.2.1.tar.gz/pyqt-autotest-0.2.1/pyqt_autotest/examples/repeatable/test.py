from pyqt_autotest.core.action import Action
from pyqt_autotest.examples.simple.usercode import UserWidget
from pyqt_autotest.repeatable_auto_test import RepeatableAutoTest


class SimpleRepeatableTest(RepeatableAutoTest):
    def setup_options(self):
        self.options.number_of_runs = 1
        self.options.wait_time = 100  # milliseconds

        self.options.sequence_of_actions = [Action.MouseLeftClick, Action.MouseLeftClick, Action.MouseLeftClick]
        self.options.sequence_of_widgets = ["Success", "Success", "Cause Exception"]

    def setup_widget(self):
        # Must instantiate the 'self.widget' member variable, and it must be a QWidget
        self.widget = UserWidget()
