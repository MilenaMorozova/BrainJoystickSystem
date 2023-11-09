from enums.status_enum import StatusEnum
from states.state_with_store import StateWithStore


class PlayerAnswerState(StateWithStore):
    status = StatusEnum.PLAYER_ANSWER

    def on_enter(self):
        self.store.question_timer.pause()
