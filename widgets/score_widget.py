from typing import Callable, Optional

from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton

from player import Player


class ScoreWidget(QWidget):
    def __init__(self, func: Callable[[int], None]):
        super().__init__()

        main_container = QHBoxLayout()

        self.__text_area = QLineEdit()
        number_validator = QIntValidator()
        self.__text_area.setValidator(number_validator)
        self.__text_area.setPlaceholderText("0")

        minus_button = QPushButton("-")
        minus_button.clicked.connect(lambda: func(-self.get_text_as_number()))

        plus_button = QPushButton("+")
        plus_button.clicked.connect(lambda: func(self.get_text_as_number()))

        main_container.addWidget(minus_button)
        main_container.addWidget(self.__text_area)
        main_container.addWidget(plus_button)

        self.setLayout(main_container)

    def get_text_as_number(self) -> int:
        text_value = self.__text_area.text().strip()
        return 0 if text_value == "" else int(text_value)
