# Project Repository : https://github.com/robertapplin/pyqt-autotest
# Authored by Robert Applin, 2022
import sys
from io import StringIO


class VerbosityController:
    """
    A class to control the amount of debug information is output to the terminal.
    """

    def __init__(self, verbose: bool):
        self._verbose = verbose

    def __enter__(self):
        """When entering a 'with' statement."""
        if not self._verbose:
            self.stdout = sys.stdout
            sys.stdout = StringIO()

    def __exit__(self, exc_type, exc_value, traceback):
        """When exiting a 'with' statement."""
        if not self._verbose:
            sys.stdout = self.stdout
            self.stdout = None
