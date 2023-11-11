import sys
import typing
from dataclasses import dataclass

from PyQt6 import QtGui
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from helpers.signals import SignalArgs
from states.state_with_store import init_all_states
from states.stop_state import StopState
from stores.store import Store
from widgets.buttons_panel import ButtonsPanel
from widgets.central_widget import CentralWidget

from widgets.players_container import PlayersContainer

MAIN_STYLE = """
    background-color: #272D2D;
"""


@dataclass
class OnResizeSignalArgs(SignalArgs):
    pass


class MainWindow(QMainWindow):
    on_resize = pyqtSignal(OnResizeSignalArgs)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Брейн ринг система")
        main_widget = QWidget()

        self._active_player_widget = CentralWidget()

        self.players_container = PlayersContainer()

        main_container = QVBoxLayout()
        main_container.setContentsMargins(0, 0, 0, 0)
        main_container.setSpacing(0)
        main_container.addWidget(self._active_player_widget)
        main_container.addLayout(self.players_container)
        main_widget.setLayout(main_container)
        self.setCentralWidget(main_widget)
        self._buttons_panel = ButtonsPanel(self)

        self.setStyleSheet(MAIN_STYLE)

    def resizeEvent(self, a0: typing.Optional[QtGui.QResizeEvent]) -> None:
        self.on_resize.emit(OnResizeSignalArgs(sender=self))

    def keyPressEvent(self, key_event: QtGui.QKeyEvent) -> None:
        if key_event.key() == Qt.Key.Key_Backspace:
            app.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    store = Store.get()
    store.game.state = StopState()
    init_all_states()

    store.input.start()

    # TODO: Solve problem with size of window
    window = MainWindow()
    # window.showFullScreen()
    window.setFixedSize(640, 480)
    window.show()
    app.exec()
