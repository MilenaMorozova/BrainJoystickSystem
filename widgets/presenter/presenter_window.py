import typing

from PyQt6 import QtGui
from PyQt6.QtCore import QSize, pyqtSignal
from PyQt6.QtWidgets import QWidget

from enums.status_enum import StatusEnum
from helpers.signals import OnResizeSignalArgs
from services.game_store import OnChangeStateSignalArgs
from services.service_locator import ServiceLocator
from widgets.presenter.lobby_presenter_widget import LobbyPresenterWidget
from widgets.presenter.player_answer_presenter_widget import PlayerAnswerPresenterWidget


class PresenterWindow(QWidget):
    on_resize = pyqtSignal(OnResizeSignalArgs)

    def __init__(self):
        super().__init__()
        # TODO: Solve problem with size of window
        self.setMinimumSize(QSize(640, 480))

        self.setWindowTitle("Окно ведущего")

        self.lobby_presenter_widget = LobbyPresenterWidget(self)
        self.player_answer_presenter_widget = PlayerAnswerPresenterWidget(self)
        self.player_answer_presenter_widget.hide()

        ServiceLocator.get().game.on_change_state.connect(self.on_change_state_handler)

    def on_change_state_handler(self, args: OnChangeStateSignalArgs):
        self.lobby_presenter_widget.hide()
        self.player_answer_presenter_widget.hide()
        if args.new_state.status == StatusEnum.LOBBY:
            self.lobby_presenter_widget.show()
        elif args.new_state.status == StatusEnum.PLAYER_ANSWER:
            self.player_answer_presenter_widget.show()

    def resizeEvent(self, a0: typing.Optional[QtGui.QResizeEvent]) -> None:
        self.on_resize.emit(OnResizeSignalArgs(sender=self))
