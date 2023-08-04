import sys
from typing import List

from PyQt6 import QtGui
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget

from joystick_button_enum import JoystickButton
from player import Player
from joystick_controller import JoystickController, JoystickDownEvent
from widgets.active_player_widget import ActivePlayerWidget
from widgets.buttons_panel import ButtonsPanel
from widgets.player_widget import PlayerWidget


class MainWindow(QMainWindow):
    on_add_player = pyqtSignal(Player)
    on_remove_player = pyqtSignal(Player)

    def __init__(self):
        super().__init__()
        self.on_add_player.connect(self.__add_player)
        self.on_remove_player.connect(self.__remove_player)

        self.setWindowTitle("My App")
        main_widget = QWidget()

        self.__buttons_panel = ButtonsPanel()

        self.__active_player_widget = ActivePlayerWidget()

        self.players_container = QHBoxLayout()
        self.__players: List[Player] = []

        main_container = QVBoxLayout()
        main_container.addLayout(self.__buttons_panel)
        main_container.addWidget(self.__active_player_widget)
        main_container.addLayout(self.players_container)
        main_widget.setLayout(main_container)
        self.setCentralWidget(main_widget)

        joystick_controller = JoystickController(self.key_joystick_event)
        joystick_controller.start()

    def keyPressEvent(self, key_event: QtGui.QKeyEvent) -> None:
        if key_event.key() == Qt.Key.Key_Backspace:
            self.close()

    def key_joystick_event(self, key: JoystickDownEvent) -> None:
        # start button - connect joystick
        match key.button_id:
            case JoystickButton.START:
                if key.joystick_id not in [i.joystick_id for i in self.__players]:
                    new_player = Player("name", key.joystick_id)
                    self.on_add_player.emit(new_player)
            case JoystickButton.BACK:
                if key.joystick_id in [i.joystick_id for i in self.__players]:
                    player = [i for i in self.__players if i.joystick_id == key.joystick_id][0]
                    self.on_remove_player.emit(player)
            case JoystickButton.A:
                if key.joystick_id in [i.joystick_id for i in self.__players]:
                    player = [i for i in self.__players if i.joystick_id == key.joystick_id][0]
                    self.__active_player_widget.on_player_click.emit(player)
            case _:
                raise ValueError(f"Unexpected value ({key.button_id})")

    def __add_player(self, player: Player):
        self.__players.append(player)
        player_widget = PlayerWidget(player)
        self.players_container.addWidget(player_widget)

    def __remove_player(self, player: Player):
        index = self.__players.index(player)
        self.__players.remove(player)
        self.players_container.itemAt(index).widget().deleteLater()


app = QApplication(sys.argv)

window = MainWindow()
window.showFullScreen()

app.exec()
