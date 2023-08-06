# Project Repository : https://github.com/robertapplin/pyqt-autotest
# Authored by Robert Applin, 2022
from configparser import ConfigParser
from os.path import expanduser, isdir
from typing import List

from pyqt_autotest.utilities.print_colors import PrintColors

HOME_DIR = expanduser("~").replace("\\", "/")
CONFIG_FILEPATH = f"{HOME_DIR}/.autotest"
OUTPUT_DIR_OPTION = "output_directory"
SECTION_HEADING = "setup"
SEARCH_DIR_OPTION = "search_directories"


def _get_multiple_directories_for_option(option_name: str) -> List[str]:
    """Returns a the output directory set by the user. It searches the config file for this directory."""
    parser = ConfigParser()
    if len(parser.read(CONFIG_FILEPATH)) == 0:
        raise RuntimeError(
            f"{PrintColors.ERROR}Please create a '{CONFIG_FILEPATH}' file, and specify the "
            f"'{SEARCH_DIR_OPTION}' option{PrintColors.END}"
        )

    if SECTION_HEADING not in parser:
        raise RuntimeError(
            f"{PrintColors.ERROR}A '{SECTION_HEADING}' section heading was not found in the "
            f"'{CONFIG_FILEPATH}' file{PrintColors.END}"
        )

    options = parser[SECTION_HEADING]
    if option_name not in options:
        raise RuntimeError(
            f"{PrintColors.ERROR}A '{option_name}' option was not found in the '{CONFIG_FILEPATH}' " f"file{PrintColors.END}"
        )

    directories_split = options[option_name].split()
    # Split by quotes in case a directory has a space inside it and so has been provided with surrounding quotes
    split_by_quotes = options[option_name].split('"')
    # Remove duplicates from list
    directories_split = list(dict.fromkeys(split_by_quotes + directories_split))
    # Replace the back-slashes with forward-slashes, and expand '~' and other characters
    directories_split = [expanduser(directory.replace("\\", "/")) for directory in directories_split]
    # Remove non-existent directories
    directories_split = [directory for directory in directories_split if isdir(directory)]

    if len(directories_split) == 0:
        raise RuntimeError(
            f"{PrintColors.ERROR}No existing directory found for the '{option_name}' option in the "
            f"'{CONFIG_FILEPATH}' file{PrintColors.END}"
        )

    return directories_split


def get_search_directories_from_config_file() -> List[str]:
    """Returns a list of directories to search for test files. It searches the config file for these directories."""
    return _get_multiple_directories_for_option(SEARCH_DIR_OPTION)


def get_output_directory_from_config_file() -> str:
    """Returns the output directory set by the user. It searches the config file for this directory."""
    output_directories = _get_multiple_directories_for_option(OUTPUT_DIR_OPTION)

    if len(output_directories) > 1:
        print(
            f"{PrintColors.WARNING}PyQtAutoTest Warning: Only one output directory is allowed, but multiple were "
            f"found. Using the first directory.{PrintColors.END}"
        )

    # Only return the first output directory, as we only output the files in one location
    return output_directories[0]
