from tempfile import TemporaryFile

from pygame.mixer import Sound


class AudioPlayer:
    def __init__(self, audio: bytes):
        self.audio = audio
        with TemporaryFile() as temp_file:
            temp_file.write(self.audio)
            temp_file.seek(0)
            self.sound = Sound(temp_file)

    def get_duration(self) -> int:
        return int(self.sound.get_length() * 1000)

    def play(self):
        self.sound.play()
