from typing import List

from packs.question import Question


class Theme:
    def __init__(self, name: str, questions: List[Question]):
        self.name = name
        self.questions = questions

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)
