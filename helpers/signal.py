from copy import copy
from typing import Set, Callable


class Signal:
    """
    Temp class for solving problem with signals in animations
    """

    def __init__(self):
        self._listeners: Set[Callable] = set()

    def connect(self, func: Callable):
        self._listeners.add(func)

    def disconnect(self, func: Callable):
        self._listeners.remove(func)

    def emit(self, *args, **kwargs):
        for listener in copy(self._listeners):
            listener(*args, **kwargs)
