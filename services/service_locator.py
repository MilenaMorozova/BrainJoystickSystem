from helpers.timer import Timer
from services.joystick_input import JoystickInput
from services.game_store import GameStore
from services.player_store import PlayerStore


class ServiceLocator:
    _instance = None

    def __init__(self):
        self.player = PlayerStore()
        self.input = JoystickInput(self.player)
        self.game = GameStore()
        self.question_timer = Timer()

    @staticmethod
    def get() -> 'ServiceLocator':
        if ServiceLocator._instance is None:
            ServiceLocator._instance = ServiceLocator()

        return ServiceLocator._instance
