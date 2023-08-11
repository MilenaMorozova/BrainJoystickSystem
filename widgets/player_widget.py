from PyQt6.QtCore import Qt, pyqtProperty, QPropertyAnimation, QSequentialAnimationGroup, pyqtSignal
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QFrame

from widgets.score_widget import ScoreWidget
from player import Player
from widgets.text_edit import TextEdit


def get_widget_style(background_color: QColor):
    return f"""
    max-height: 200;
    background-color: rgb({background_color.red()}, {background_color.green()}, {background_color.blue()});
"""


LABEL_STYLE = """
    color: white;
    font-size: 28px;
"""


class PlayerWidget(QFrame):
    on_click_a = pyqtSignal()

    def __init__(self, player: Player):
        super().__init__()
        self.player = player
        self.on_click_a.connect(self.start_blinking)
        self.player.signals.on_change_name.connect(self.change_player_name_handler)

        self.main_container = QVBoxLayout()

        self.name_label = QLabel(player.name)
        self.name_label.setStyleSheet(LABEL_STYLE)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_label.mouseDoubleClickEvent = self.double_click_to_name_label_handler

        self.main_container.addWidget(self.name_label)

        self.name_edit = TextEdit()
        self.name_edit.editingFinished.connect(self.editing_finished_name_edit_handler)
        self.name_edit.hide()
        self.main_container.addWidget(self.name_edit)

        self.setLayout(self.main_container)

        self.__score = 0
        self.score_label = QLabel(str(self.__score))
        self.score_label.setStyleSheet(LABEL_STYLE)
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_container.addWidget(self.score_label)

        score_widget = ScoreWidget(self.update_score)
        self.main_container.addWidget(score_widget)

        self.setStyleSheet(get_widget_style(player.color))

        #for_animation
        self._background_color = player.color
        self._anim = None

    def update_score(self, value: int):
        self.score += value

    @property
    def score(self) -> int:
        return self.__score

    @score.setter
    def score(self, value: int):
        self.__score = value
        self.score_label.setText(str(self.__score))

    def double_click_to_name_label_handler(self, event):
        self.name_label.hide()
        self.name_edit.setText(self.player.name)
        self.name_edit.show()
        self.name_edit.setFocus()

    def editing_finished_name_edit_handler(self):
        self.name_edit.hide()
        self.player.name = self.name_edit.text()
        self.name_label.show()

    def change_player_name_handler(self, old_name: str, new_name: str):
        self.name_label.setText(new_name)

    # for animations
    @pyqtProperty(QColor)
    def background_color(self):
        return self._background_color

    @background_color.setter
    def background_color(self, value):
        self._background_color = value
        style = f"""
            max-height: 200;
            background-color: rgb({self._background_color.red()}, {self._background_color.green()}, {self._background_color.blue()});
        """
        self.setStyleSheet(style)

    def start_blinking(self):
        self.anim = QPropertyAnimation(self, b"background_color")
        self.anim.setEndValue(QColor("white"))
        self.anim.setDuration(120)
        self.anim2 = QPropertyAnimation(self, b"background_color")
        self.anim2.setEndValue(self.player.color)
        self.anim2.setDuration(120)
        self.anim3 = QPropertyAnimation(self, b"background_color")
        self.anim3.setEndValue(QColor("white"))
        self.anim3.setDuration(120)
        self.anim4 = QPropertyAnimation(self, b"background_color")
        self.anim4.setEndValue(self.player.color)
        self.anim4.setDuration(120)
        self.anim_group = QSequentialAnimationGroup()
        self.anim_group.addAnimation(self.anim)
        self.anim_group.addAnimation(self.anim2)
        self.anim_group.addAnimation(self.anim3)
        self.anim_group.addAnimation(self.anim4)
        self.anim_group.start()
