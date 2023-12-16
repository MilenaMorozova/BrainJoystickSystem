from enums.status_enum import StatusEnum
from states.state_with_service_locator import StateWithServiceLocator


class QuestionState(StateWithServiceLocator):
    status = StatusEnum.QUESTION

    def on_enter(self):
        self.locator.question_timer.start()
