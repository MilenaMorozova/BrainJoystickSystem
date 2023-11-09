from enums.joystick_button_enum import JoystickButton
from enums.status_enum import StatusEnum
from joystick_input import OnPlayerClickSignalArgs, OnNotPlayerClickSignalArgs
from states.state_with_store import StateWithStore


class StoppedState(StateWithStore):
    status = StatusEnum.STOPPED

    def on_click_play(self):
        self.store.question_timer.set_max_time(10)
        self._to(StatusEnum.STARTED)

    def on_enter(self):
        self.store.question_timer.pause()

        self.store.input.on_player_click.connect(self._on_player_click_handler)
        self.store.input.on_not_player_click.connect(self._on_not_player_click_handler)

    def on_exit(self):
        self.store.input.on_player_click.disconnect(self._on_player_click_handler)
        self.store.input.on_not_player_click.disconnect(self._on_not_player_click_handler)

    def _on_player_click_handler(self, args: OnPlayerClickSignalArgs):
        match args.key:
            case JoystickButton.BACK:
                self.store.player.remove_player(args.player)

    def _on_not_player_click_handler(self, args: OnNotPlayerClickSignalArgs):
        match args.key:
            case JoystickButton.START:
                self.store.player.create_player(args.joystick_id)
