from typing import List

from packs.theme import Theme


class Round:
    def __init__(self, name: str, themes: List[Theme], is_final: bool = False):
        self.name = name
        self.themes = themes
        self.is_final = is_final

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Round):
            return False

        return (
                self.name == other.name and
                self.themes == other.themes
        )
