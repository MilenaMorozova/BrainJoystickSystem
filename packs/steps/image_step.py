from packs.steps.question_step import QuestionStep


class ImageStep(QuestionStep):
    def get_result(self) -> bytes:
        return self.loader.load_image(self.get_filename())
