from enums.joystick_button_enum import JoystickButton
from enums.status_enum import StatusEnum
from joystick_input import OnPlayerClickSignalArgs
from states.state_with_store import StateWithStore


class StartedState(StateWithStore):
    status = StatusEnum.STARTED

    def on_enter(self):
        self.store.question_timer.start()
        self.store.input.on_player_click.connect(self._on_player_click)

    def on_exit(self):
        self.store.input.on_player_click.disconnect(self._on_player_click)

    def on_click_play(self):
        self._to(StatusEnum.PAUSED)

    def on_click_reset(self):
        self._to(StatusEnum.STOPPED)

    def _on_player_click(self, args: OnPlayerClickSignalArgs):
        if args.key == JoystickButton.A:
            self.store.game.active_player = args.player
            self._to(StatusEnum.PLAYER_ANSWER)

