from typing import Callable

import pygame
from PyQt6.QtCore import QThread


class JoystickDownEvent:
    def __init__(self, joystick_id: int, button_id: int):
        self.button_id = button_id
        self.joystick_id = joystick_id

    def __str__(self):
        return f"button_id: {self.button_id}, joystick_id: {self.joystick_id}"


class JoystickController:
    def __init__(self, on_button_press: Callable[[JoystickDownEvent], None]):
        pygame.init()
        pygame.joystick.init()
        self.__joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        self.on_button_press = on_button_press

    def __handle_event(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.JOYBUTTONDOWN:
                    joystick_down_event = JoystickDownEvent(event.joy, event.button)
                    self.on_button_press(joystick_down_event)

    def start(self):
        thread1 = JoystickThread(target=self.__handle_event)
        thread1.start()


class JoystickThread(QThread):
    def __init__(self, target: Callable):
        super().__init__()
        self.target = target

    def run(self) -> None:
        self.target()
