from enums.status_enum import StatusEnum
from states.state_with_service_locator import StateWithServiceLocator


class PauseState(StateWithServiceLocator):
    status = StatusEnum.PAUSE

    def on_enter(self):
        self.locator.question_timer.pause()

    def on_click_play(self):
        self._set_next_state(StatusEnum.RUN)
