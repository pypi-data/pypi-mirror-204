# Project Repository : https://github.com/robertapplin/pyqt-autotest
# Authored by Robert Applin, 2022
from os.path import join
from typing import Type

from pyqt_autotest.cli.config import get_output_directory_from_config_file, get_search_directories_from_config_file
from pyqt_autotest.cli.modules import find_files_in_directories, get_matching_tests_in_module, search_file_for_test_classes
from pyqt_autotest.cli.options import Options
from pyqt_autotest.core.exception_handler import catch_exceptions
from pyqt_autotest.qt.application import get_application
from pyqt_autotest.utilities.print_colors import PrintColors
from pyqt_autotest.utilities.verbosity_controller import VerbosityController
from pyqt_autotest.results.json_results_dict import JSONResultsDict
from pyqt_autotest.results.print_results import print_results

app = get_application()


def _find_matching_tests(regex: str, python_files, verbosity_controller: VerbosityController):
    """Returns a list of tests that match the provided regex."""
    matching_tests = []
    with verbosity_controller:
        for directory, filenames in python_files.items():
            for filename in filenames:
                module, test_classes, import_str = search_file_for_test_classes(f"{directory}/{filename}")
                matching_tests.extend(get_matching_tests_in_module(regex, filename, test_classes, import_str))
    return matching_tests


def _run_test(
    test_name: str,
    test_class: Type,
    import_str: str,
    number_of_runs: int,
    number_of_actions: int,
    wait_time: int,
    verbose: bool,
    verbosity_controller: VerbosityController,
) -> None:
    """Runs the tests in a module if the tests match a regex."""
    print(f"{PrintColors.INFO}Running '{test_name}'...{PrintColors.END}\n")
    options = Options(number_of_runs, number_of_actions, wait_time, verbose)
    instance = test_class[1](options, verbosity_controller)
    instance._run(test_name, import_str)


@catch_exceptions
def run(
    regex: str, number_of_runs: int, number_of_actions: int, wait_time: int, output_name: str, cautious: bool, verbose: bool
) -> None:
    """Runs the tests with the provided options."""
    global app

    json_results = JSONResultsDict()
    json_results.cautious = cautious
    if output_name is not None:
        json_results.output_filepath = join(get_output_directory_from_config_file(), output_name) + ".json"

    verbosity_controller = VerbosityController(verbose)

    python_files = find_files_in_directories(get_search_directories_from_config_file(), "py")
    matching_tests = _find_matching_tests(regex, python_files, verbosity_controller)

    if len(matching_tests) == 0:
        print(f"{PrintColors.ERROR}No matching tests were found for regex '{regex}'." f"{PrintColors.END}")
        return

    for test_name, test_class, import_str in matching_tests:
        _run_test(
            test_name, test_class, import_str, number_of_runs, number_of_actions, wait_time, verbose, verbosity_controller
        )

    json_results.save_to_file()
    print_results(json_results.output_filepath)
