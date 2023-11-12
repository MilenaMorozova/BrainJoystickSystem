from enums.status_enum import StatusEnum
from states.state_with_store import StateWithStore


class PauseState(StateWithStore):
    status = StatusEnum.PAUSE

    def on_enter(self):
        self.store.question_timer.pause()

    def on_click_play(self):
        self._set_next_state(StatusEnum.RUN)

    def on_click_reset(self):
        self._set_next_state(StatusEnum.STOP)
