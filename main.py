import random
import sys
import typing
from dataclasses import dataclass
from typing import List

from PyQt6 import QtGui
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget

from helpers.signals import SignalArgs
from joystick_button_enum import JoystickButton
from player import Player
from joystick_controller import JoystickController, JoystickDownEvent
from widgets.active_player_widget import ActivePlayerWidget
from widgets.buttons_panel import ButtonsPanel
from widgets.player_widget import PlayerWidget, OnClickASignalHandler

COLORS = [
    QColor('#F1495C'),  # pink
    QColor('#F69A39'),  # orange
    QColor('#F9DE27'),  # yellow
    QColor('#75BC6A'),  # green
    QColor('#5891F6'),  # blue
    QColor('#BA75DA'),  # purple
]

MAIN_STYLE = """
    background-color: #272D2D;
"""


@dataclass
class OnAddPlayerSignalArgs(SignalArgs):
    player: Player


@dataclass
class OnRemovePlayerSignalArgs(SignalArgs):
    player: Player


@dataclass
class OnResizeSignalArgs(SignalArgs):
    pass


@dataclass
class OnPlayerClickSignalArgs(SignalArgs):
    player: Player


class MainWindow(QMainWindow):
    on_add_player = pyqtSignal(OnAddPlayerSignalArgs)
    on_remove_player = pyqtSignal(OnRemovePlayerSignalArgs)
    on_resize = pyqtSignal(OnResizeSignalArgs)

    def __init__(self):
        super().__init__()
        self.on_add_player.connect(self.__add_player_signal_handler)
        self.on_remove_player.connect(self.__remove_player_signal_handler)

        self.setWindowTitle("Брейн ринг система")
        main_widget = QWidget()

        self.__active_player_widget = ActivePlayerWidget()

        self.players_container = QHBoxLayout()
        self.players_container.setContentsMargins(0, 0, 0, 0)
        self.players_container.setSpacing(10)
        self.__players: List[Player] = []

        main_container = QVBoxLayout()
        main_container.setContentsMargins(0, 0, 0, 0)
        main_container.setSpacing(0)
        main_container.addWidget(self.__active_player_widget)
        main_container.addLayout(self.players_container)
        main_widget.setLayout(main_container)
        self.setCentralWidget(main_widget)
        self.__buttons_panel = ButtonsPanel(self)

        self.setStyleSheet(MAIN_STYLE)

        joystick_controller = JoystickController(self.key_joystick_event)
        joystick_controller.start()

    def keyPressEvent(self, key_event: QtGui.QKeyEvent) -> None:
        if key_event.key() == Qt.Key.Key_Backspace:
            app.quit()

    def resizeEvent(self, a0: typing.Optional[QtGui.QResizeEvent]) -> None:
        self.on_resize.emit(OnResizeSignalArgs(sender=self))

    def key_joystick_event(self, key: JoystickDownEvent) -> None:
        # start button - connect joystick
        match key.button_id:
            case JoystickButton.START:
                if key.joystick_id not in [i.joystick_id for i in self.__players]:
                    new_player = Player(f"Имя {len(self.players_container) + 1}", key.joystick_id, self.get_new_color())
                    self.on_add_player.emit(OnAddPlayerSignalArgs(sender=self, player=new_player))
            case JoystickButton.BACK:
                if key.joystick_id in [i.joystick_id for i in self.__players]:
                    player = [i for i in self.__players if i.joystick_id == key.joystick_id][0]
                    self.on_remove_player.emit(OnRemovePlayerSignalArgs(sender=self, player=player))
            case JoystickButton.A:
                if key.joystick_id in [i.joystick_id for i in self.__players]:
                    player = [i for i in self.__players if i.joystick_id == key.joystick_id][0]
                    self.get_player_widget(player).on_click_a.emit(OnClickASignalHandler(sender=self))
                    self.__active_player_widget.on_player_click.emit(
                        OnPlayerClickSignalArgs(sender=self, player=player)
                    )
            case _:
                raise ValueError(f"Unexpected value ({key.button_id})")

    def __add_player_signal_handler(self, args: OnAddPlayerSignalArgs):
        self.__players.append(args.player)
        player_widget = PlayerWidget(args.player)
        self.players_container.addWidget(player_widget)

    def get_new_color(self) -> str:
        def color_is_free(color: str) -> bool:
            return not any([i.color == color for i in self.__players])
        pos_colors = list(filter(color_is_free, COLORS))
        if not pos_colors:
            pos_colors = COLORS
        return random.choice(pos_colors)

    def __remove_player_signal_handler(self, args: OnRemovePlayerSignalArgs):
        index = self.__players.index(args.player)
        self.__players.remove(args.player)
        self.players_container.itemAt(index).widget().deleteLater()

    def get_player_widget(self, player: Player) -> PlayerWidget:
        index = self.__players.index(player)
        return self.players_container.itemAt(index).widget()


app = QApplication(sys.argv)

# TODO разобраться с размером экрана
window = MainWindow()
#window.showFullScreen()
window.show()
app.exec()
