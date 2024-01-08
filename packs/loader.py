from typing import Optional
from zipfile import ZipFile


class Loader:
    def __init__(self, path: str):
        self.path = path
        self.archive: Optional[ZipFile] = None

    def load(self):
        self.archive = ZipFile(self.path, 'r')

    def get_content(self) -> bytes:
        return self.archive.read('content.xml')

    def load_image(self, filename: str) -> bytes:
        return self.archive.read(f'Images/{filename}')

    def load_audio(self, filename: str) -> bytes:
        return self.archive.read(f'Audio/{filename}')

    def load_video(self, filename: str) -> bytes:
        return self.archive.read(f'Video/{filename}')
