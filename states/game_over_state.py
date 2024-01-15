from enums.status_enum import StatusEnum
from states.state_with_service_locator import StateWithServiceLocator


class GameOverState(StateWithServiceLocator):
    status = StatusEnum.GAME_OVER
