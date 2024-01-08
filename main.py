import sys

from PyQt6.QtWidgets import QApplication

from helpers.tempfiles import delete_all_temp_files
from states.state_with_service_locator import init_all_states
from states.lobby_state import LobbyState
from services.service_locator import ServiceLocator
from widgets.main_window import MainWindow
from widgets.presenter.presenter_window import PresenterWindow

if __name__ == '__main__':
    delete_all_temp_files()
    app = QApplication(sys.argv)

    services = ServiceLocator.get()
    services.game.state = LobbyState()
    init_all_states()
    services.input.start()

    main_window = MainWindow()
    presenter_window = PresenterWindow()

    main_window.show()
    presenter_window.show()
    app.exec()
    delete_all_temp_files()
