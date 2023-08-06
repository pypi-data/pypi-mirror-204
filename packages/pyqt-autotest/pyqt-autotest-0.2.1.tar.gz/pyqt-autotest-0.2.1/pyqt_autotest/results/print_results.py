# Project Repository : https://github.com/robertapplin/pyqt-autotest
# Authored by Robert Applin, 2022
from pyqt_autotest.results.exit_state import ExitState
from pyqt_autotest.results.json_results_dict import JSONResultsDict
from pyqt_autotest.results.statistic_finder import StatisticFinder
from pyqt_autotest.utilities.print_colors import PrintColors


def print_results(output_filepath: str = "") -> None:
    """Prints the results of the tests to the terminal."""
    stat_finder = StatisticFinder(JSONResultsDict())
    number_of_successes = stat_finder.count_exit_state(ExitState.Success)
    number_of_warnings = stat_finder.count_exit_state(ExitState.Warning)
    number_of_errors = stat_finder.count_exit_state(ExitState.Error)

    print(
        f"Successes ({PrintColors.SUCCESS}{number_of_successes}{PrintColors.END}) | "
        f"Warnings ({PrintColors.WARNING}{number_of_warnings}{PrintColors.END}) | "
        f"Errors ({PrintColors.ERROR}{number_of_errors}{PrintColors.END})\n"
    )

    if output_filepath is None:
        return
    if output_filepath != "":
        print(f"A PyQt AutoTest output file has successfully been created:\n\n\t{output_filepath}\n")
