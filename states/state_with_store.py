from typing import Dict, Type

from enums.status_enum import StatusEnum
from states.base_state import BaseState
from stores.store import Store


_STATES: Dict[StatusEnum, Type[BaseState]] = {}


class StateWithStore(BaseState):
    def __init__(self):
        self.store = Store.get()

    def _set_next_state(self, status: StatusEnum):
        global _STATES

        if status in _STATES:
            self.store.game.state = _STATES[status]()
        else:
            raise Exception(f"Status = {status.name} not registered, pls add new Status to {init_all_states.__name__}")


def init_all_states():
    from states.pause_state import PauseState
    from states.player_answer_state import PlayerAnswerState
    from states.run_state import RunState
    from states.stop_state import StopState
    global _STATES

    _STATES = {
        StatusEnum.PAUSE: PauseState,
        StatusEnum.PLAYER_ANSWER: PlayerAnswerState,
        StatusEnum.RUN: RunState,
        StatusEnum.STOP: StopState,
    }
