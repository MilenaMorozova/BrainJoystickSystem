from typing import Callable

from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton

from widgets.text_edit import TextEdit

BUTTON_STYLE = """
    color: white;
    font-size: 38px;
    font-weight: bold;
    min-width: 40px;
    max-width: 40px;
    min-height: 40px;
    max-height: 40px;
    margin-bottom: 10px;
    border: none;
"""


class ScoreWidget(QWidget):
    def __init__(self, func: Callable[[int], None]):
        super().__init__()

        main_container = QHBoxLayout()

        self.__text_area = TextEdit()
        number_validator = QIntValidator()
        self.__text_area.setValidator(number_validator)
        self.__text_area.setPlaceholderText("0")

        minus_button = QPushButton("-")
        minus_button.setStyleSheet(BUTTON_STYLE)
        minus_button.clicked.connect(lambda: func(-self.get_text_as_number()))

        plus_button = QPushButton("+")
        plus_button.setStyleSheet(BUTTON_STYLE)
        plus_button.clicked.connect(lambda: func(self.get_text_as_number()))

        main_container.addWidget(minus_button)
        main_container.addWidget(self.__text_area)
        main_container.addWidget(plus_button)

        self.setLayout(main_container)

    def get_text_as_number(self) -> int:
        text_value = self.__text_area.text().strip()
        return 0 if text_value == "" else int(text_value)
