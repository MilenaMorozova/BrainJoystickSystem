from packs.steps.question_step import QuestionStep


class TextStep(QuestionStep):
    def get_result(self) -> str:
        return self.content
