import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PySide2.QtCore import Qt
from app import stream_chat

from .chat_gui import ChatWindow

class LauncherWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Program Launcher")
        self.setMinimumSize(300, 200)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        chat_button = QPushButton("Chat")
        chat_button.clicked.connect(self.launch_chat)
        layout.addWidget(chat_button)

        # Add buttons for other programs here

        self.central_widget.setLayout(layout)

    def launch_chat(self):
        stream_chat()