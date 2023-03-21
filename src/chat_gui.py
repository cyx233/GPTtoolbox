import sys
from PySide2.QtWidgets import  QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit, QPushButton
from PySide2.QtCore import Qt 
from PySide2.QtGui import QTextCursor
import threading

class ChatWindow(QMainWindow):
    def __init__(self, chat_client, chat_thread):
        super().__init__()
        self.chat_client = chat_client 
        self.chat_thread = chat_thread
        self.chat_thread.message_received.connect(self.handle_message)
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Chat")
        self.setMinimumSize(600, 400)
        self.central_widget = QWidget()
        self.message_log = QTextEdit()
        self.message_log.setReadOnly(True)
        self.message_input = QLineEdit()
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.handle_send)
        layout = QVBoxLayout()
        layout.addWidget(self.message_log)
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.message_input)
        input_layout.addWidget(self.send_button)
        layout.addLayout(input_layout)
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)
        self.message_input.setFocus()

    def handle_send(self):
        message = self.message_input.text()
        self.handle_message("User:\n")
        self.handle_message(message)
        self.handle_message("\n\n")
        succ = self.chat_client.send(message)
        if succ:
            self.message_input.clear()
        else:
            self.handle_message("Send Failed!\n")

    def handle_message(self, message):
        self.message_log.moveCursor(QTextCursor.End)
        self.message_log.insertPlainText(message)
        self.message_log.moveCursor(QTextCursor.End)