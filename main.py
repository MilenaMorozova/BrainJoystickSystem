import sys
from typing import Callable

from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QLineEdit


class ScoreWidget(QWidget):
    def __init__(self, func: Callable[[int], None]):
        super().__init__()
        main_container = QHBoxLayout()

        minus_button = QPushButton("-")
        text_area = QLineEdit()
        minus_button.clicked.connect(lambda: func(-int(text_area.text())))
        main_container.addWidget(minus_button)

        main_container.addWidget(text_area)

        plus_button = QPushButton("+")
        plus_button.clicked.connect(lambda: func(int(text_area.text())))
        main_container.addWidget(plus_button)

        self.setLayout(main_container)


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
        gamer_name_label = QLabel("Hello")
        gamer_name_label.setStyleSheet("background-color: #000000; color: #FFFFFF;")

        main_container.addWidget(gamer_name_label)

        gamers_container = QHBoxLayout()
        gamer1 = GamerButton("gamer1")
        gamers_container.addWidget(gamer1)

        gamer2 = GamerButton("gamer2")
        gamers_container.addWidget(gamer2)

        main_container.addLayout(gamers_container)

        main_widget.setLayout(main_container)
        self.setCentralWidget(main_widget)

    def keyPressEvent(self, key_event: QtGui.QKeyEvent) -> None:
        if key_event.key() == Qt.Key.Key_Escape:
            self.close()


app = QApplication(sys.argv)

window = MainWindow()
window.showFullScreen()

app.exec()
