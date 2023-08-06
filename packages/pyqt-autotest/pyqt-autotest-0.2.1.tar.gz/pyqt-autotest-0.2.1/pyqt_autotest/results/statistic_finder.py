# Project Repository : https://github.com/robertapplin/pyqt-autotest
# Authored by Robert Applin, 2022
from pyqt_autotest.results.exit_state import ExitState
from pyqt_autotest.results.json_results_dict import JSONResultsDict
from pyqt_autotest.results.result_schema import RUN_EXIT_STATE_KEY, RUNS_KEY


class StatisticFinder:
    def __init__(self, result_dict: JSONResultsDict):
        self._results_dict = result_dict

    def count_exit_state(self, exit_state: ExitState) -> int:
        """Count the number of runs with a particular exit state."""
        return len(
            [
                run_result
                for test_result in self._results_dict.values()
                for run_result in test_result[RUNS_KEY]
                if run_result[RUN_EXIT_STATE_KEY] == exit_state.value
            ]
        )
