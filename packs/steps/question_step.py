from packs.loader import Loader


class QuestionStep:
    def __init__(self, content: str, loader: Loader):
        self.content = content
        self.loader = loader

    def get_result(self):
        raise NotImplemented()

    def __str__(self):
        return self.content

    def __repr__(self):
        return str(self)
