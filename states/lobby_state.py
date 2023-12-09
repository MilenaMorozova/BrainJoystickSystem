from typing import Optional

from animations.start_game_animation import StartGameAnimation
from enums.joystick_button_enum import JoystickButton
from enums.status_enum import StatusEnum
from helpers.player_generator import PlayerGenerator
from joystick_input import OnPlayerClickSignalArgs, OnUnknownPlayerClickSignalArgs
from states.state_with_store import StateWithStore


class LobbyState(StateWithStore):
    status = StatusEnum.LOBBY

    def __init__(self):
        super().__init__()
        self._player_generator = PlayerGenerator(self.store.player)
        self._start_game_animation: Optional[StartGameAnimation] = None

    def on_enter(self):
        self.store.input.on_player_click.connect(self._on_player_click_handler)
        self.store.input.on_unknown_player_click.connect(self._on_unknown_player_click_handler)

    def on_exit(self):
        self.store.input.on_player_click.disconnect(self._on_player_click_handler)
        self.store.input.on_unknown_player_click.disconnect(self._on_unknown_player_click_handler)

    def _on_player_click_handler(self, args: OnPlayerClickSignalArgs):
        match args.key:
            case JoystickButton.BACK:
                self.store.player.remove_player(args.player)

    def _on_unknown_player_click_handler(self, args: OnUnknownPlayerClickSignalArgs):
        match args.key:
            case JoystickButton.START:
                self.store.player.add_player(
                    player=self._player_generator.get_new_player(joystick_id=args.joystick_id)
                )

    def on_click_play(self):
        self._start_game_animation = StartGameAnimation()
        self._set_next_state_after_animation(StatusEnum.CHOICE_QUESTION, self._start_game_animation)
