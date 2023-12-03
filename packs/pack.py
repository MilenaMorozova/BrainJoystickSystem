from typing import List

from packs.round import Round


class Pack:
    def __init__(self, name: str, version: str, restriction: str,
                 created: str, tags: str, rounds: List[Round]):
        self.name = name
        self.version = version
        self.restriction = restriction
        self.created = created
        self.tags = tags
        self.rounds = rounds

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Pack):
            return False

        return (
                self.name == other.name and
                self.version == other.version and
                self.restriction == other.restriction and
                self.tags == other.tags and
                self.rounds == other.rounds
        )
