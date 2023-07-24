import sys
from typing import Callable, List

from PyQt6 import QtGui
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QLineEdit

from joystick_button_enum import JoystickButton
from player import Player
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


class PlayerWidget(QWidget):
    def __init__(self, player: Player):
        super().__init__()
        main_container = QVBoxLayout()

        name_label = QLabel(player.name)
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
    on_new_player = pyqtSignal(Player)

    def __init__(self):
        super().__init__()
        self.on_new_player.connect(self.__add_player)

        self.setWindowTitle("My App")
        main_widget = QWidget()

        main_container = QVBoxLayout()
        self.__player_name = QLabel("Hello")
        self.__player_name.setStyleSheet("background-color: #000000; color: #FFFFFF;")

        main_container.addWidget(self.__player_name)
        self.players_container = QHBoxLayout()

        self.__players: List[Player] = []

        main_container.addLayout(self.players_container)

        main_widget.setLayout(main_container)
        self.setCentralWidget(main_widget)

        joystick_controller = JoystickController(self.key_joystick_event)
        joystick_controller.start()

    def keyPressEvent(self, key_event: QtGui.QKeyEvent) -> None:
        self.__player_name.setText(str(key_event.key()))

        if key_event.key() == Qt.Key.Key_Escape:
            self.close()

    def key_joystick_event(self, key: JoystickDownEvent) -> None:
        # start button - connect joystick
        if key.button_id == JoystickButton.START \
                and key.joystick_id not in [i.joystick_id for i in self.__players]:
            new_player = Player("name", key.joystick_id)
            self.on_new_player.emit(new_player)

    def __add_player(self, player: Player):
        self.__players.append(player)
        # player_widget = PlayerWidget(player)
        self.players_container.addWidget(QLabel("new player"))


app = QApplication(sys.argv)

window = MainWindow()
window.showFullScreen()

app.exec()
