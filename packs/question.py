from typing import List

from packs.steps.question_step import QuestionStep


class Question:
    def __init__(self, steps_before: List[QuestionStep], steps_after: List[QuestionStep], answer: str, price: int):
        self.steps_before = steps_before
        self.steps_after = steps_after
        self.answer = answer
        self.price = price
        self.is_answered = False

    def __str__(self):
        return self.answer

    def __repr__(self):
        return str(self)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Question):
            return False

        return (
                self.steps_before == other.steps_before and
                self.steps_after == other.steps_after and
                self.answer == other.answer and
                self.price == other.price
        )
