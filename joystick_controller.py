from dataclasses import dataclass
from threading import Thread
from typing import Callable

import pygame

from joystick_button_enum import JoystickButton


@dataclass
class JoystickDownEvent:
    button_id: JoystickButton
    joystick_id: int

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
                if event.type == pygame.JOYBUTTONDOWN and event.button in list(JoystickButton):
                    joystick_down_event = JoystickDownEvent(
                        button_id=JoystickButton(event.button),
                        joystick_id=event.joy
                    )
                    self.on_button_press(joystick_down_event)

    def start(self):
        thread = Thread(target=self.__handle_event)
        thread.start()
