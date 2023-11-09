from helpers.timer import Timer
from joystick_input import JoystickInput
from stores.game_store import GameStore
from stores.player_store import PlayerStore


class Store:
    _instance = None

    def __init__(self):
        self.player = PlayerStore()
        self.input = JoystickInput(self.player)
        self.game = GameStore()
        self.question_timer = Timer()

    @staticmethod
    def get() -> 'Store':
        if Store._instance is None:
            Store._instance = Store()

        return Store._instance
