from packs.steps.question_step import QuestionStep


class AudioStep(QuestionStep):

    def get_result(self) -> bytes:
        return self.loader.load_audio(self.get_filename())
