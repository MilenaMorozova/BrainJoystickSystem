from packs.steps.question_step import QuestionStep


class VideoStep(QuestionStep):

    def get_result(self) -> bytes:
        return self.loader.load_video(self.get_filename())

