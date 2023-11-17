from typing import Optional, Callable

from enums.status_enum import StatusEnum
from states.state_with_store import StateWithStore


class WaitAnimationState(StateWithStore):
    status = StatusEnum.WAIT_ANIMATION

    def __init__(self):
        super().__init__()
        self.on_end_animation: Optional[Callable] = None
