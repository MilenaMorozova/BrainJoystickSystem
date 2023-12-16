from enums.joystick_button_enum import JoystickButton
from enums.status_enum import StatusEnum
from services.joystick_input import OnPlayerClickSignalArgs
from states.state_with_service_locator import StateWithServiceLocator


class RunState(StateWithServiceLocator):
    status = StatusEnum.RUN

    def on_enter(self):
        self.locator.question_timer.start()
        self.locator.input.on_player_click.connect(self._on_player_click)

    def on_exit(self):
        self.locator.input.on_player_click.disconnect(self._on_player_click)

    def on_click_play(self):
        self._set_next_state(StatusEnum.PAUSE)

    def _on_player_click(self, args: OnPlayerClickSignalArgs):
        if args.key == JoystickButton.A:
            self.locator.game.active_player = args.player
            self._set_next_state(StatusEnum.PLAYER_ANSWER)

