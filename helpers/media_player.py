import os
from tempfile import TemporaryFile
from typing import Optional

from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtWidgets import QWidget

from settings import TEMP_FILES_PREFIX


class MediaPlayer:
    def __init__(self, video_output: Optional[QWidget] = None):
        self.video_output = video_output

        self.audio_output = QAudioOutput()
        self.audio_output.setVolume(0.1)

        self.media_player = QMediaPlayer()
        self.media_player.setVideoOutput(video_output)
        self.media_player.setAudioOutput(self.audio_output)

        self.temp_file = None

    def __del__(self):
        self.clean_cache()

    def set_content(self, content: bytes):
        self.clean_cache()
        self.temp_file = TemporaryFile(delete=False, prefix=TEMP_FILES_PREFIX)
        self.temp_file.write(content)
        self.temp_file.close()
        self.media_player.setSource(QUrl.fromLocalFile(self.temp_file.name))

    def get_duration(self) -> int:
        return self.media_player.duration()

    def clean_cache(self):
        self.media_player.setSource(QUrl(''))
        if self.temp_file:
            os.remove(self.temp_file.name)
            self.temp_file = None

    def play(self):
        self.media_player.play()
