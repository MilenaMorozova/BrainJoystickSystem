from enums.status_enum import StatusEnum
from states.state_with_service_locator import StateWithServiceLocator


class PlayerAnswerState(StateWithServiceLocator):
    status = StatusEnum.PLAYER_ANSWER

    def on_enter(self):
        self.locator.question_timer.pause()
