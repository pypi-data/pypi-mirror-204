# pyqt-autotest ⚙️🧪
A command line tool for finding system-level bugs that cause a python Qt application to terminate. This is achieved by simulating user actions on a widget using [QtTest](https://doc.qt.io/qt-5/qtest-overview.html).

This tool requires you to provide a python class which inherits from the provided `RandomAutoTest` class. The widget defined inside this class will be opened a specified number of times, and a random selection of actions is performed on the children widgets within the encompassing widget. The result of each run is recorded, and warnings/errors are captured, before a report is generated to provide reliable instructions for how to reproduce a bug.

## Table of contents
* [Installation](#installation)
* [Setup](#setup)
* [Options](#options)
* [Test class](#test-class)
* [Built-in Actions](#built-in-actions)
* [Creating your own Actions](#creating-your-own-actions)
* [Usage](#usage)
* [Output](#output)

## Installation

This package can be installed from [PyPI](https://pypi.org/project/pyqt-autotest/) using pip.

```sh
pip install pyqt-autotest
```

## Setup

Create a file named `.autotest` in your home directory with the following contents.

```
[setup]
search_directories = /path/to/test/directory1/
                     /path/to/test/directory2/
output_directory = /path/to/output/directory/
```

The `search_directories` option is used to specify the directories to search for python files containing your test classes. The `output_directory` option is used to specify the directory to store the output results in.

## Options

The following table details the options that can be provided on the command line.

| Option            | Description                                                                                                                                 | Default                      | Command line option     |
|-------------------|---------------------------------------------------------------------------------------------------------------------------------------------|------------------------------|-------------------------|
| Tests regex       | Run tests matching this regular expression. The directories provided in the `.autotest` configuration file are searched for matching tests. |                              | -R, --tests-regex       |
| List tests        | Flag which lists the tests that are found in the search directories specified by the `.autotest` configuration file. The tests are not run. | False                        | -l, --list-tests        |
| Number of runs    | The number of times to open the widget and perform a random selection of actions.                                                           | 1                            | -n, --number-of-runs    |
| Number of actions | The number of random actions to perform each time the widget is opened.                                                                     | 10                           | -a, --number-of-actions |
| Wait time         | The number of milliseconds to wait between executing two consecutive actions.                                                               | 50                           | -w, --wait-time         |
| Output name       | The name to give the output file. The output file is stored in the output_directory specified by the `.autotest` configuration file.        | No output file is generated. | -o, --output-name       |
| Cautious          | Flag which saves the output file before each action is performed. This ensures an output file is still created after a terminating fault.   | False                        | -c, --cautious          |
| Verbose           | Flag which prints more debug information when supplied. It also prints the actions just before each of them is performed.                   | False                        | -v, --verbose           |

## Test class

The first thing to do is to create a python class which inherits from `RandomAutoTest`, and implement the `setup_widget` method. Inside this method, you should instantiate your `QWidget` and assign it to the member variable `self.widget`as follows. Any additional setup, such as loading data into your widget, should also be done in the same method.

```py
from usercode.model import ExampleModel
from usercode.presenter import ExamplePresenter
from usercode.view import ExampleView

from pyqt_autotest.random_auto_test import RandomAutoTest


class ExampleTest(RandomAutoTest):

    def setup_widget(self):
        # The 'self.widget' member variable MUST be instantiated, and it must be a QWidget.
        self.widget = ExampleView()

        # Other relevant setup should be done here too. This example refers to the Model-View-Presenter (MVP) pattern
        self.model = ExampleModel()
        self.presenter = ExamplePresenter(self.widget, self.model)

        # Your test might be more interesting if you first load data into the widget
        self.presenter.load_data("fake_data_file.dat")
```

Optionally, you can also create a `setup_options` method to specify commonly used options. However, these options will be overridden if provided on the command line. Note that the `Output Name` option cannot be provided in this setup method.

```py
    def setup_options(self):
        self.options.number_of_runs = 2
        self.options.number_of_actions = 15
        self.options.wait_time = 200  # milliseconds
```

## Built-in Actions

The following actions are built-in to this package. Only these actions can be performed if you do not create your own (see the section below on [how to create your own](#creating-your-own-actions)).

| Built-in Action       | Description                                               | Python Callable                                          |
|-----------------------|-----------------------------------------------------------|----------------------------------------------------------|
| Action.KeyDownClick   | Simulates the Down key being pressed on an active widget. | `lambda widget: QTest.keyClick(widget, Qt.Key_Down)`     |
| Action.KeyUpClick     | Simulates the Up key being pressed on an active widget.   | `lambda widget: QTest.keyClick(widget, Qt.Key_Up)`       |
| Action.MouseLeftClick | Simulates a widget being left clicked by the mouse.       | `lambda widget: QTest.mouseClick(widget, Qt.LeftButton)` |

These actions will by default be performed for the following widget types. This has been made minimalistic on purpose because this command line tool is arguably more useful if you carefully customize your own actions as seen in the next section.

| Widget type       | Built-in Actions      |
|-------------------|-----------------------|
| QPushButton       | Action.MouseLeftClick |

## Creating your own Actions
This package provides a great amount of flexibility for you to create and customize the actions you want to be available during a 'random auto test'. It also allows you to ignore certain widget types by not providing any actions for them.

The following code provides a basic example for how to define your own custom actions:

```py
    def setup_options(self):
        # The 'actions' dictionary requires a string to describe an action, and a callable function which uses QtTest to
        # perform an action. Note that the 'Left click in centre' action is useful for testing a QCheckBox.
        actions = {
            "Enter dummy text": lambda widget: QTest.keyClicks(widget, "dummy text"),
            "Left click in centre": lambda widget: QTest.mouseClick(widget, Qt.LeftButton,
                                                                    pos=QPoint(2, widget.height() / 2))
        }

        # The 'widget_actions' dictionary requires you to specify which actions can be performed on which widget types.
        # Note that you can use the built-in actions, or create your own with a string name. The string name is used to
        # describe what an action does when generating the output instructions, so make sure it is short but descriptive.
        widget_actions = {
            QCheckBox: ["Left click in centre"],
            QLineEdit: ["Enter dummy text"],
            QSpinBox: [Action.KeyDownClick, Action.KeyUpClick]
        }

        # This will overwrite the built-in actions. You could use 'dict::update' to keep the built-in actions.
        self.options.actions = actions
        self.options.widget_actions = widget_actions
```

## Usage

It is trivial to run your test class from the command line as follows (depending on its module location):

```sh
autotest -R ExampleTest
```
or with more arguments:
```
autotest -R ExampleTest -n 5 -a 10 -w 150 -o autotest_results -v
```

## Output

An output json file will only be generated if an `Output Name` is provided from the command line using the `-o, --output-name` option. Alternatively, you can use the `Verbose` flag to get debug information from your terminal using the `-v, --verbose` option.
