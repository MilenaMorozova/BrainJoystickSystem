import sys

from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget


class GamerButton(QWidget):
    def __init__(self, name: str):
        super().__init__()
        main_container = QVBoxLayout()

        gamer_name_label = QLabel(name)
        main_container.addWidget(gamer_name_label)

        self.setLayout(main_container)
        self.setMaximumHeight(200)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        main_widget = QWidget()

        main_container = QVBoxLayout()
        gamer_name_label = QLabel("Hello")
        gamer_name_label.setStyleSheet("background-color: #000000; color: #FFFFFF;")

        main_container.addWidget(gamer_name_label)

        gamers_container = QHBoxLayout()
        gamer1 = GamerButton("gamer1")
        gamers_container.addWidget(gamer1)

        gamer2 = GamerButton("gamer2")
        gamers_container.addWidget(gamer2)

        main_container.addLayout(gamers_container)

        main_widget.setLayout(main_container)
        self.setCentralWidget(main_widget)

    def keyPressEvent(self, key_event: QtGui.QKeyEvent) -> None:
        if key_event.key() == Qt.Key.Key_Escape:
            self.close()


app = QApplication(sys.argv)

window = MainWindow()
window.showFullScreen()

app.exec()
