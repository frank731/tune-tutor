import time
import matplotlib.pyplot as plt
import sys
from audio_handler import AudioHandler
from PyQt6.QtWidgets import QApplication, QPushButton, QMainWindow, QLabel, QVBoxLayout, QWidget
from threading import Thread

#TODO make something that can detect "base" chord at point in song and match with your playing at same point, make time stamps of chord switches, maybe use that library chord smth

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.microphone = None
        self.label = QLabel("Detected chord: ")
        self.start_button = QPushButton("Start recording")
        self.start_button.clicked.connect(self.startMicrophone)
        self.stop_button = QPushButton("Stop recording")
        self.stop_button.clicked.connect(self.stopMicrophone)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.stop_button)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def updateChord(self, newChord):
        self.label.setText("Detected chord: " + newChord)

    def startMicrophone(self):
        self.microphone = AudioHandler(self.updateChord)
        self.microphone.start()     # open the the stream
    
    def stopMicrophone(self):
        self.microphone.stop()

app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
