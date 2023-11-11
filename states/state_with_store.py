from typing import Dict, Type

from enums.status_enum import StatusEnum
from states.state import State
from stores.store import Store


_STATES: Dict[StatusEnum, Type[State]] = {}


class StateWithStore(State):
    def __init__(self):
        self.store = Store.get()

    def _to(self, status: StatusEnum):
        global _STATES

        if status in _STATES:
            self.store.game.state = _STATES[status]()
        else:
            raise Exception(f"Status = {status.name} not registered, pls add new Status to {init_all_states.__name__}")


def init_all_states():
    from states.paused_state import PausedState
    from states.player_answer_state import PlayerAnswerState
    from states.started_state import StartedState
    from states.stopped_state import StoppedState
    global _STATES

    _STATES = {
        StatusEnum.PAUSED: PausedState,
        StatusEnum.PLAYER_ANSWER: PlayerAnswerState,
        StatusEnum.STARTED: StartedState,
        StatusEnum.STOPPED: StoppedState,
    }
