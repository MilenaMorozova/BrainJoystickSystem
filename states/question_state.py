from enums.joystick_button_enum import JoystickButton
from enums.status_enum import StatusEnum
from services.joystick_input import OnPlayerClickSignalArgs
from states.state_with_service_locator import StateWithServiceLocator


class QuestionState(StateWithServiceLocator):
    status = StatusEnum.QUESTION

    def on_enter(self):
        self.locator.question_timer.start()
        self.locator.input.on_player_click.connect(self._on_player_click_handler)

    def on_exit(self):
        self.locator.question_timer.pause()
        self.locator.input.on_player_click.disconnect(self._on_player_click_handler)

    def _on_player_click_handler(self, args: OnPlayerClickSignalArgs):
        if args.key == JoystickButton.A and self.locator.game.active_player is None:
            self.locator.game.active_player = args.player
            self._set_next_state(StatusEnum.PLAYER_ANSWER)
