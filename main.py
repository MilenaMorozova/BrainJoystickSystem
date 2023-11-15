import sys

from PyQt6.QtWidgets import QApplication

from states.state_with_store import init_all_states
from states.stop_state import StopState
from stores.store import Store
from widgets.admin.admin_window import AdminWindow
from widgets.main_window import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)

    store = Store.get()
    store.game.state = StopState()
    init_all_states()
    store.input.start()

    main_window = MainWindow()
    admin_window = AdminWindow()

    main_window.show()
    admin_window.show()
    app.exec()
