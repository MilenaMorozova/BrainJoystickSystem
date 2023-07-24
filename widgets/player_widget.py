from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

from widgets.score_widget import ScoreWidget
from player import Player


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
