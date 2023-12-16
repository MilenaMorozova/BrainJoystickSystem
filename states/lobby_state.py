from threading import Thread
from typing import Optional

from animations.start_game_animation import StartGameAnimation
from enums.joystick_button_enum import JoystickButton
from enums.status_enum import StatusEnum
from helpers.player_generator import PlayerGenerator
from services.joystick_input import OnPlayerClickSignalArgs, OnUnknownPlayerClickSignalArgs
from packs.parser import Parser
from states.state_with_service_locator import StateWithServiceLocator


class LobbyState(StateWithServiceLocator):
    status = StatusEnum.LOBBY

    def __init__(self):
        super().__init__()
        self._player_generator = PlayerGenerator(self.locator.player)
        self._start_game_animation: Optional[StartGameAnimation] = None

    def on_enter(self):
        self.locator.input.on_player_click.connect(self._on_player_click_handler)
        self.locator.input.on_unknown_player_click.connect(self._on_unknown_player_click_handler)

    def on_exit(self):
        self.locator.input.on_player_click.disconnect(self._on_player_click_handler)
        self.locator.input.on_unknown_player_click.disconnect(self._on_unknown_player_click_handler)

    def load_pack_async(self, path: str):
        def func():
            parser = Parser(path)
            parser.load()
            self.locator.game.pack = parser.get_pack()

        thread = Thread(target=func)
        thread.start()

    def _on_player_click_handler(self, args: OnPlayerClickSignalArgs):
        match args.key:
            case JoystickButton.BACK:
                self.locator.player.remove_player(args.player)

    def _on_unknown_player_click_handler(self, args: OnUnknownPlayerClickSignalArgs):
        match args.key:
            case JoystickButton.START:
                self.locator.player.add_player(
                    player=self._player_generator.get_new_player(joystick_id=args.joystick_id)
                )

    def on_click_play(self):
        self._start_game_animation = StartGameAnimation()
        self._set_next_state_after_animation(StatusEnum.CHOICE_QUESTION, self._start_game_animation)
