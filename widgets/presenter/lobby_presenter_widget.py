from PyQt6.QtWidgets import QWidget

from enums.status_enum import StatusEnum
from services.service_locator import ServiceLocator
from widgets.presenter.buttons.play_button import PlayButton
from widgets.presenter.buttons.select_pack_button import SelectPackButton


class LobbyPresenterWidget(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.game_store = ServiceLocator.get().game

        self.play_button = PlayButton(self)
        self.play_button.move(20, 20)
        self.play_button.hide()

        self.select_pack_button = SelectPackButton(self)
        self.select_pack_button.move(20, 20)

        self.game_store.on_change_pack.connect(self.update_buttons)
        self.game_store.on_change_state.connect(self.update_buttons)

    def update_buttons(self, *args, **kwargs):
        if self.game_store.state.status == StatusEnum.LOBBY and self.game_store.pack is not None:
            self.play_button.show()
        else:
            self.play_button.hide()

        if self.game_store.state.status == StatusEnum.LOBBY and self.game_store.pack is None:
            self.select_pack_button.show()
        else:
            self.select_pack_button.hide()

