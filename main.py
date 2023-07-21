import sys
from typing import Callable

from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QLineEdit
import pygame

from joystick_controller import JoystickController, JoystickDownEvent


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


class GamerButton(QWidget):
    def __init__(self, name: str):
        super().__init__()
        main_container = QVBoxLayout()

        name_label = QLabel(name)
        main_container.addWidget(name_label)

        self.setLayout(main_container)
        self.setMaximumHeight(200)

        self.__score = 0
        self.__score_label = QLabel(str(self.__score))
        main_container.addWidget(self.__score_label)

        score_widget = ScoreWidget(self.update_score)
        main_container.addWidget(score_widget)

    def update_score(self, value: int):
        self.score += value

    @property
    def score(self) -> int:
        return self.__score

    @score.setter
    def score(self, value: int):
        self.__score = value
        self.__score_label.setText(str(self.__score))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        main_widget = QWidget()

        main_container = QVBoxLayout()
        self.__gamer_name = QLabel("Hello")
        self.__gamer_name.setStyleSheet("background-color: #000000; color: #FFFFFF;")

        main_container.addWidget(self.__gamer_name)

        gamers_container = QHBoxLayout()
        gamer1 = GamerButton("gamer1")
        gamers_container.addWidget(gamer1)

        gamer2 = GamerButton("gamer2")
        gamers_container.addWidget(gamer2)

        main_container.addLayout(gamers_container)

        main_widget.setLayout(main_container)
        self.setCentralWidget(main_widget)

        joystick_controller = JoystickController(self.key_joystick_event)
        joystick_controller.start()

    def keyPressEvent(self, key_event: QtGui.QKeyEvent) -> None:
        self.__gamer_name.setText(str(key_event.key()))

        if key_event.key() == Qt.Key.Key_Escape:
            self.close()

    def key_joystick_event(self, key: JoystickDownEvent) -> None:
        self.__gamer_name.setText(str(key))


app = QApplication(sys.argv)

window = MainWindow()
window.showFullScreen()

app.exec()
