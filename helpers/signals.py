from dataclasses import dataclass


@dataclass
class SignalArgs:
    sender: object


@dataclass
class OnResizeSignalArgs(SignalArgs):
    pass
