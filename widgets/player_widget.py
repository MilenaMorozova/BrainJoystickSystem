from PyQt6.QtCore import Qt, pyqtProperty, QPropertyAnimation, QSequentialAnimationGroup
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QFrame

from enums.joystick_button_enum import JoystickButton
from services.joystick_input import OnPlayerClickSignalArgs
from services.service_locator import ServiceLocator
from widgets.score_widget import ScoreWidget
from player import Player, OnChangeNameSignalArgs, OnChangeScoreSignalArgs
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

    def __init__(self, player: Player):
        super().__init__()
        self.player = player
        self._input = ServiceLocator.get().input
        self._input.on_player_click.connect(self._on_player_click)
        self.player.on_change_name.connect(self._on_change_player_name_handler)
        self.player.on_change_score.connect(self._on_change_score_handler)

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

        self.score_label = QLabel(str(player.score))
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
        self.player.score += value

    def double_click_to_name_label_handler(self, event):
        self.name_label.hide()
        self.name_edit.setText(self.player.name)
        self.name_edit.show()
        self.name_edit.setFocus()

    def editing_finished_name_edit_handler(self):
        self.name_edit.hide()
        self.player.name = self.name_edit.text()
        self.name_label.show()

    def _on_change_player_name_handler(self, args: OnChangeNameSignalArgs):
        self.name_label.setText(args.new_name)

    def _on_change_score_handler(self, args: OnChangeScoreSignalArgs):
        self.score_label.setText(str(args.new_score))

    def _on_player_click(self, args: OnPlayerClickSignalArgs):
        if args.player == self.player and args.key == JoystickButton.A:
            self.start_blinking()

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

    def __del__(self):
        self._input.on_player_click.disconnect(self._on_player_click)
        self.player.on_change_name.disconnect(self._on_change_player_name_handler)
        self.player.on_change_score.disconnect(self._on_change_score_handler)