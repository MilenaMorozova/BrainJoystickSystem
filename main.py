import sys

from PyQt6.QtWidgets import QApplication

from states.state_with_store import init_all_states
from states.lobby_state import LobbyState
from stores.store import Store
from widgets.main_window import MainWindow
from widgets.presenter.presenter_window import PresenterWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    store = Store.get()
    store.game.state = LobbyState()
    init_all_states()
    store.input.start()

    main_window = MainWindow()
    presenter_window = PresenterWindow()

    main_window.show()
    presenter_window.show()
    app.exec()
