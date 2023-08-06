# Project Repository : https://github.com/robertapplin/pyqt-autotest
# Authored by Robert Applin, 2022
from typing import List, Tuple

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget

EXCLUDE_TOP_LEVEL_CLASSES = ["QComboBoxPrivateContainer"]


def get_widget_class_and_text(widget: QWidget) -> Tuple[str, str]:
    """Return the widgets class and text."""
    text = widget.text() if callable(getattr(widget, "text", None)) else ""
    class_name = widget.metaObject().className()
    return class_name, text


def get_top_level_widget_list_as_str() -> str:
    """Returns a string listing the top level widgets."""
    widget_strs = []
    for widget in QApplication.topLevelWidgets():
        class_name, text = get_widget_class_and_text(widget)
        if class_name not in EXCLUDE_TOP_LEVEL_CLASSES:
            widget_strs.append(class_name if text == "" else f"{class_name} with text '{text}'")

    return "\n\t\t".join(widget_strs)


def get_top_level_widget_classes() -> List[str]:
    """Returns a list of top level widget class names."""
    top_level_widget_classes = []
    for widget in QApplication.topLevelWidgets():
        class_name = widget.metaObject().className()
        if class_name not in EXCLUDE_TOP_LEVEL_CLASSES:
            top_level_widget_classes.append(class_name)
    return top_level_widget_classes


def clear_top_level_widgets() -> None:
    """Close and delete all existing top level widgets."""
    for widget in QApplication.topLevelWidgets():
        widget.setAttribute(Qt.WA_DeleteOnClose)
        widget.close()
