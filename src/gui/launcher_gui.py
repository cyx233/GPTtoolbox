import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PySide2.QtCore import Qt
from app import stream_chat

from .chat_gui import ChatWindow

class LauncherWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Program Launcher")
        self.setMinimumSize(400, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        chat_button = QPushButton("Chat")
        chat_button.clicked.connect(self.launch_chat)

        layout.addWidget(chat_button)

        # Add buttons for other programs here
        self.central_widget.setLayout(layout)
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Adjust font size based on window height
        font_size = min(max(self.height() // 15, 1), 20)
        font = self.central_widget.font()
        font.setPointSize(font_size)
        self.central_widget.setFont(font)

    def launch_chat(self):
        stream_chat()