# Project Repository : https://github.com/robertapplin/pyqt-autotest
# Authored by Robert Applin, 2022
from schema import And, Schema, Use

AUTO_TEST_TYPE_KEY = "auto_test_type"
IMPORTS_KEY = "imports"
SETUP_KEY = "setup"
NUMBER_OF_RUNS_KEY = "number_of_runs"
NUMBER_OF_ACTIONS_KEY = "number_of_actions"
WAIT_TIME_KEY = "wait_time"
RUNS_KEY = "runs"

RUN_ACTIONS_KEY = "actions"
RUN_WIDGETS_KEY = "widgets"
RUN_EXIT_STATE_KEY = "exit_state"
RUN_MESSAGE_KEY = "message"

# The schema used for validating the results of a single test (with or without multiple runs)
RESULT_SCHEMA = Schema(
    {
        AUTO_TEST_TYPE_KEY: And(Use(str)),
        IMPORTS_KEY: And(Use(str)),
        SETUP_KEY: And(Use(str)),
        NUMBER_OF_RUNS_KEY: And(Use(int)),
        NUMBER_OF_ACTIONS_KEY: And(Use(int)),
        WAIT_TIME_KEY: And(Use(int)),
        RUNS_KEY: [
            {RUN_ACTIONS_KEY: [str], RUN_WIDGETS_KEY: [str], RUN_EXIT_STATE_KEY: And(Use(str)), RUN_MESSAGE_KEY: And(Use(str))}
        ],
    }
)
