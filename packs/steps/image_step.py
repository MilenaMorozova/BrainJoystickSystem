from packs.steps.question_step import QuestionStep


class ImageStep(QuestionStep):
    def get_result(self) -> bytes:
        filename = self.content[1:]
        return self.loader.load_image(filename)
