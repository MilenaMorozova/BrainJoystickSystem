from enums.status_enum import StatusEnum
from joystick_input import OnPlayerClickSignalArgs
from states.state_with_store import StateWithStore


class PausedState(StateWithStore):
    status = StatusEnum.PAUSED

    def on_enter(self):
        self.store.question_timer.pause()

    def on_click_play(self):
        self._to(StatusEnum.STARTED)

    def on_click_reset(self):
        self._to(StatusEnum.STOPPED)
