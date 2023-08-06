# Project Repository : https://github.com/robertapplin/pyqt-autotest
# Authored by Robert Applin, 2022
import re
from importlib.util import module_from_spec, spec_from_file_location
from inspect import getmembers, isclass
from os import listdir
from os.path import splitext
from typing import Dict, List, Tuple, Type
from pyqt_autotest.random_auto_test import RandomAutoTest
from pyqt_autotest.repeatable_auto_test import RepeatableAutoTest
from pyqt_autotest.utilities.print_colors import PrintColors

BASE_TEST_CLASSES = [RandomAutoTest.__name__, RepeatableAutoTest.__name__]


def find_files_in_directories(directories: List[str], extension: str) -> Dict[str, List[str]]:
    """Returns the python files stored in particular directories."""
    result = {}
    for directory in directories:
        result[directory] = [file for file in listdir(directory) if file.endswith(extension)]
    return result


def search_file_for_imports(filepath: str) -> str:
    """Searches for the imports in a file and returns them as a string."""
    with open(filepath, "r") as file:
        all_lines = file.readlines()

    import_lines = ""
    for line in all_lines:
        if "import" in line and RandomAutoTest.__name__ not in line:
            import_lines += line
    return import_lines


def search_file_for_test_classes(filepath: str):
    """Imports a python module and checks if it contains at least one test class. It returns any found test classes."""
    print(f"Checking '{filepath}' for test classes...")

    try:
        # Import module
        spec = spec_from_file_location("", filepath)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception as ex:
        print(f"{PrintColors.ERROR}{str(ex)}{PrintColors.END}")
        return None, None, None
    else:
        # Find test classes inside the module
        test_classes = getmembers(
            module,
            lambda member: isclass(member) and (issubclass(member, RandomAutoTest) or issubclass(member, RepeatableAutoTest)),
        )
        # Find import lines inside the module
        import_str = search_file_for_imports(filepath)
        # Remove classes with a base test type
        test_classes = [cls for cls in test_classes if cls[0] not in BASE_TEST_CLASSES]
        if len(test_classes) == 0:
            print(
                f"{PrintColors.WARNING}Failed to find a test class which inherits from one of '{BASE_TEST_CLASSES}'."
                f"{PrintColors.END}"
            )
            return None, None, None
        return module, test_classes, import_str


def get_test_name(filename: str, test_class: Tuple[str, Type]) -> str:
    """Constructs the name of a test"""
    return f"{splitext(filename)[0]}_{test_class[0]}"


def does_module_and_class_match_regex(regex: str, test_name: str) -> bool:
    """Returns true if the regex is found inside the test name."""
    pattern = re.compile(regex)
    return re.search(pattern, test_name)


def get_matching_tests_in_module(regex: str, filename: str, test_classes: List[Tuple[str, Type]], import_str: str):
    """Returns the test classes that match a particular regex."""
    matching_tests = []
    if test_classes is not None:
        for test_class in test_classes:
            test_name = get_test_name(filename, test_class)
            if does_module_and_class_match_regex(regex, test_name):
                matching_tests.append((test_name, test_class, import_str))
    return matching_tests
