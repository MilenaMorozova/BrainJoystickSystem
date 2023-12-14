from enums.status_enum import StatusEnum
from states.state_with_store import StateWithStore


class QuestionState(StateWithStore):
    status = StatusEnum.QUESTION

    def on_enter(self):
        self.store.question_timer.start()
