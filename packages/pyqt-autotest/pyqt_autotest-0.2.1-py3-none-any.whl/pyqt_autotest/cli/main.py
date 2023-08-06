# Project Repository : https://github.com/robertapplin/pyqt-autotest
# Authored by Robert Applin, 2022
from pyqt_autotest.cli.options import DEFAULT_NUMBER_OF_RUNS, DEFAULT_NUMBER_OF_ACTIONS, DEFAULT_WAIT_TIME
from pyqt_autotest.cli.list_tests import print_matching_tests
from pyqt_autotest.cli.run_tests import run

import argparse
import sys


def get_parser():
    """
    Create and return a parser for capturing the command line arguments.
    :return: configured argument parser
    :rtype: argparse.ArgParser
    """

    epilog = """
Usage Examples:

    $ autotest -R RandomTest -l
    $ autotest -R SimpleRandomTest
    $ autotest -R SimpleRandomTest -n 5 -a 10 -w 500 -o simpletest_out

For more information on this package, please see the documentation pages found in the pyqt-autotest Github repository.
"""

    parser = argparse.ArgumentParser(
        prog="PyQtAutoTest", add_help=True, epilog=epilog, formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "-R",
        "--tests-regex",
        metavar="TESTS_REGEX",
        help="Run tests matching this regular expression. The directories provided in the .autotest "
        "configuration file are searched for matching tests.",
    )

    parser.add_argument(
        "-l",
        "--list-tests",
        action="store_true",
        help="Flag which lists the tests that are found in the search directories specified by the "
        "`.autotest` configuration file. The tests are not run.",
    )

    parser.add_argument(
        "-n",
        "--number-of-runs",
        metavar="NUMBER_OF_RUNS",
        help=f"The number of times to open the widget and perform a random selection of actions. "
        f"(Default = {DEFAULT_NUMBER_OF_RUNS})",
    )
    parser.add_argument(
        "-a",
        "--number-of-actions",
        metavar="NUMBER_OF_ACTIONS",
        help=f"The number of random actions to perform each time the widget is opened. "
        f"(Default = {DEFAULT_NUMBER_OF_ACTIONS})",
    )
    parser.add_argument(
        "-w",
        "--wait-time",
        metavar="WAIT_TIME",
        help=f"The number of milliseconds to wait between executing two consecutive actions. "
        f"(Default = {DEFAULT_WAIT_TIME})",
    )
    parser.add_argument(
        "-o",
        "--output-name",
        metavar="OUTPUT_NAME",
        help="The name to give the output file. It is stored in the output directory specified by "
        "the .autotest configuration file. (Default = No output file is generated)",
    )

    parser.add_argument(
        "-c",
        "--cautious",
        action="store_true",
        help="Flag which saves the output file before each action is performed. This ensures an output "
        "file is still created after a terminating fault.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Flag which prints more debug information when supplied. It also prints the actions just "
        "before each of them is performed.",
    )

    return parser


def main():
    """
    Entry point to be exposed as the `autotest` command.
    """
    parser = get_parser()
    args = parser.parse_args(sys.argv[1:])

    regex = args.tests_regex if args.tests_regex is not None else ""
    verbose = args.verbose if args.verbose else False
    if args.list_tests:
        print_matching_tests(regex, verbose)
    else:
        run(
            regex,
            number_of_runs=args.number_of_runs,
            number_of_actions=args.number_of_actions,
            wait_time=args.wait_time,
            output_name=args.output_name,
            cautious=args.cautious,
            verbose=verbose,
        )
