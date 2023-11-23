from typing import List

from packs.steps.question_step import QuestionStep


class Question:
    def __init__(self, steps_before: List[QuestionStep], steps_after: List[QuestionStep], answer: str, price: int):
        self.steps_before = steps_before
        self.steps_after = steps_after
        self.answer = answer
        self.price = price

    def __str__(self):
        return self.answer

    def __repr__(self):
        return str(self)
