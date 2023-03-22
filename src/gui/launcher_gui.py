from PySide2.QtWidgets import ( QMainWindow, QWidget, QVBoxLayout, 
                                QHBoxLayout, QPushButton, QDialog, 
                                QMessageBox, QFileDialog)
from PySide2.QtCore import QSettings
from app import stream_chat, db_chat
from utils import config_file

from .chat_gui import ChatWindow
from .config_gui import ConfigDialog 


class LauncherWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Program Launcher")
        self.setMinimumSize(400, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        chat_button = QPushButton("Chat")
        chat_button.clicked.connect(self.launch_stream_chat)

        db_chat_button = QPushButton("Chat on DB")
        db_chat_button.clicked.connect(self.launch_db_chat)

        config_button = QPushButton("Config")
        config_button.clicked.connect(self.show_config_dialog)

        layout.addWidget(chat_button)
        layout.addWidget(db_chat_button)
        layout.addWidget(config_button)

        settings = QSettings(config_file, QSettings.IniFormat)

        # Add buttons for other programs here
        self.central_widget.setLayout(layout)
        self.central_widget.setStyleSheet(f"font-size: {settings.value('settings/font_size', '18')}pt")
    
    def launch_stream_chat(self):
        stream_chat()

    def launch_db_chat(self):
        db_chat()
    
    def show_config_dialog(self):
        dialog = ConfigDialog(parent=self)
        if dialog.exec_() == QDialog.Accepted:
            QMessageBox.information(self, "Information", "Config saved. Some settings require reloading.")