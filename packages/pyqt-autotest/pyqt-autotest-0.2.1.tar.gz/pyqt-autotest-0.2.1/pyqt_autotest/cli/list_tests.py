# Project Repository : https://github.com/robertapplin/pyqt-autotest
# Authored by Robert Applin, 2022
from typing import List, Tuple, Type

from pyqt_autotest.cli.config import get_search_directories_from_config_file
from pyqt_autotest.cli.modules import (
    does_module_and_class_match_regex,
    find_files_in_directories,
    get_test_name,
    search_file_for_test_classes,
)
from pyqt_autotest.qt.application import get_application
from pyqt_autotest.utilities.print_colors import PrintColors
from pyqt_autotest.utilities.verbosity_controller import VerbosityController

app = get_application()


def _get_module_tests(regex: str, filename: str, test_classes: List[Tuple[str, Type]]) -> List[str]:
    """Gets the names of tests in a module if the tests match a regex."""
    test_names = []
    if test_classes is not None:
        for test_class in test_classes:
            test_name = get_test_name(filename, test_class)
            if regex is None or does_module_and_class_match_regex(regex, test_name):
                test_names.append(test_name)
    return test_names


def print_matching_tests(regex: str, verbose: bool) -> None:
    """Print the names of tests matching a regex found in the search directories."""
    verbosity_controller = VerbosityController(verbose)

    python_files = find_files_in_directories(get_search_directories_from_config_file(), "py")

    found_tests = {}
    with verbosity_controller:
        for directory, filenames in python_files.items():
            found_tests[directory] = []
            for filename in filenames:
                _, test_classes, _ = search_file_for_test_classes(f"{directory}/{filename}")
                found_tests[directory].extend(_get_module_tests(regex, filename, test_classes))

    number_of_tests = sum([len(val) for val in found_tests.values()])
    print(
        f"\n{PrintColors.SUCCESS}Found {number_of_tests} test(s):{PrintColors.END}\n"
        if number_of_tests > 0
        else f"\n{PrintColors.WARNING}No regex matches found{PrintColors.END}\n"
    )

    if number_of_tests > 0:
        # Find the length of the longest test name
        max_name_len = max([len(max(test_names, key=len)) for test_names in found_tests.values() if len(test_names) > 0])

        for directory, names in found_tests.items():
            for name in names:
                print(f"\t{PrintColors.INFO}{name}{' ' * (max_name_len - len(name))}{PrintColors.END}\t{directory}")
        print("\n")
