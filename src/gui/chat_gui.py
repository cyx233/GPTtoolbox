import sys
from PySide2.QtWidgets import  (QMainWindow, QWidget, QVBoxLayout, 
                                QHBoxLayout, QLineEdit, QTextEdit, 
                                QPushButton, QApplication)
from PySide2.QtCore import Qt 
from PySide2.QtGui import QTextCursor
import threading
from utils import get_config 

class ChatWindow(QMainWindow):
    def __init__(self, chat_client, chat_thread):
        super().__init__()
        self.chat_client = chat_client 
        self.chat_thread = chat_thread
        self.chat_thread.message_received.connect(self.handle_message)
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Chat")
        self.setMinimumSize(1200, 800)
        self.central_widget = QWidget()
        self.central_widget.setStyleSheet(f"font-size: {get_config('settings', 'font_size')}pt")

        self.message_log = QTextEdit()
        self.message_log.setReadOnly(True)
        self.message_log.setAcceptRichText(False)

        self.message_input = QTextEdit()
        self.message_input.setAcceptRichText(False)
        self.message_input.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.message_input.textChanged.connect(self.resize_input)
        self.message_input.setPlaceholderText("Type your message here...")
        self.message_input.setMaximumHeight(37)

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

    def resize_input(self):
        doc = self.message_input.document()
        height = doc.size().height()
        height = min(height, self.height() // 2)
        self.message_input.setMaximumHeight(height)

    def handle_send(self):
        message = self.message_input.toPlainText()
        self.handle_message("User:\n")
        self.handle_message(message)
        self.handle_message("\n\n")
        self.message_input.clear()
        QApplication.processEvents()
        succ = self.chat_client.send(message)
        if not succ:
            self.handle_message("Send Failed!\n\n")

    def handle_message(self, message):
        self.message_log.moveCursor(QTextCursor.End)
        self.message_log.insertPlainText(message)
        self.message_log.moveCursor(QTextCursor.End)