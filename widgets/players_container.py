from typing import List

from PyQt6.QtWidgets import QHBoxLayout

from stores.player_store import OnAddPlayerSignalArgs, OnRemovePlayerSignalArgs
from stores.store import Store
from widgets.player_widget import PlayerWidget


class PlayersContainer(QHBoxLayout):
    def __init__(self):
        super().__init__()

        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(10)

        self._player_widgets: List[PlayerWidget] = []
        self._players_store = Store.get().player
        self._players_store.on_add_player.connect(self._on_add_player_handler)
        self._players_store.on_remove_player.connect(self._on_remove_player_handler)

    def _on_add_player_handler(self, args: OnAddPlayerSignalArgs):
        player_widget = PlayerWidget(args.player)
        self._player_widgets.append(player_widget)
        self.addWidget(player_widget)

    def _on_remove_player_handler(self, args: OnRemovePlayerSignalArgs):
        index, player_widget = [
            (i, widget) for i, widget in enumerate(self._player_widgets) if widget.player == args.player
        ][0]
        self._player_widgets.remove(player_widget)
        self.itemAt(index).widget().deleteLater()
