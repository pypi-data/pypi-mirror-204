# Project Repository : https://github.com/robertapplin/pyqt-autotest
# Authored by Robert Applin, 2022
from json import dump
from typing import List

from pyqt_autotest.cli.options import Options
from pyqt_autotest.results.exit_state import ExitState
from pyqt_autotest.results.result_schema import (
    AUTO_TEST_TYPE_KEY,
    IMPORTS_KEY,
    NUMBER_OF_ACTIONS_KEY,
    NUMBER_OF_RUNS_KEY,
    RESULT_SCHEMA,
    RUN_ACTIONS_KEY,
    RUN_EXIT_STATE_KEY,
    RUN_MESSAGE_KEY,
    RUN_WIDGETS_KEY,
    RUNS_KEY,
    SETUP_KEY,
    WAIT_TIME_KEY,
)
from pyqt_autotest.utilities.singleton import Singleton


class JSONResultsDict(dict, metaclass=Singleton):
    _cautious: bool = False

    _test_running: bool = False
    _active_test_name: str = None

    _output_filepath: str = None

    @property
    def cautious(self) -> bool:
        """Returns the cautious flag value."""
        return self._cautious

    @cautious.setter
    def cautious(self, cautious: bool) -> None:
        """Sets the cautious flag to true or false."""
        self._cautious = cautious

    @property
    def output_filepath(self) -> str:
        """Returns the output filepath of the file to save."""
        return self._output_filepath

    @output_filepath.setter
    def output_filepath(self, filepath: str) -> None:
        """Sets the output filepath of the file to save."""
        self._output_filepath = filepath

    def init_test(self, test_type: str, import_str: str, setup_str: str, test_name: str, options: Options) -> None:
        """Initializes a new test result dictionary."""
        new_test = {
            AUTO_TEST_TYPE_KEY: test_type,
            IMPORTS_KEY: import_str,
            SETUP_KEY: setup_str,
            NUMBER_OF_RUNS_KEY: options.number_of_runs,
            NUMBER_OF_ACTIONS_KEY: options.number_of_actions,
            WAIT_TIME_KEY: options.wait_time,
            RUNS_KEY: [],
        }
        self._active_test_name = test_name
        self[self._active_test_name] = new_test

    def init_run(self) -> None:
        """Initializes a new run result dictionary."""
        new_run = {
            RUN_WIDGETS_KEY: [],
            RUN_ACTIONS_KEY: [],
            # If the run terminates, we want to record that there was an error, so set this as the initial state.
            RUN_EXIT_STATE_KEY: "Error",
            RUN_MESSAGE_KEY: "The run terminated before completing. Please use the -v, --verbose flag to debug.",
        }
        self[self._active_test_name][RUNS_KEY].append(new_run)
        self._test_running = True

    def is_running(self) -> bool:
        """Returns true if a test run is currently active."""
        return self._test_running

    def save_run_result(self, exit_state: ExitState, message: List[str] = "") -> None:
        """Stores the run as a result when the run ends."""
        if self._active_test_name not in self:
            raise RuntimeError(f"Something went wrong, the '{self._active_test_name}' property could not be found.")
        if RUNS_KEY not in self[self._active_test_name]:
            raise RuntimeError(f"Something went wrong, the '{RUNS_KEY}' property could not be found.")

        self[self._active_test_name][RUNS_KEY][-1][RUN_EXIT_STATE_KEY] = exit_state.value
        self[self._active_test_name][RUNS_KEY][-1][RUN_MESSAGE_KEY] = f"\n{''.join(message)}"

        # Allow this to fail if the results don't match the schema
        RESULT_SCHEMA.validate(self[self._active_test_name])

        self._test_running = False

    def save_event(self, widget_name: str, event_name: str) -> None:
        """Stores an event in the active run."""
        self[self._active_test_name][RUNS_KEY][-1][RUN_WIDGETS_KEY].append(widget_name)
        self[self._active_test_name][RUNS_KEY][-1][RUN_ACTIONS_KEY].append(event_name)

        instruction_number = len(self[self._active_test_name][RUNS_KEY][-1][RUN_WIDGETS_KEY])
        print(f"\t\t{instruction_number}. {event_name} the '{widget_name}' widget")

        # If in cautious mode, save the results after each event is recorded. This is expensive, but might be necessary
        # to find a bug causing a segmentation or termination fault.
        if self._cautious:
            self.save_to_file()

    def save_to_file(self):
        """Saves the results in this singleton to a json file."""
        if self.output_filepath is not None:
            with open(self.output_filepath, "w") as out_file:
                dump(self, out_file, indent=2)
