from PySide2.QtWidgets import  (QMainWindow, QWidget, QVBoxLayout, 
                                QHBoxLayout, QLineEdit, QTextEdit, 
                                QPushButton, QApplication, QListWidget,
                                QAbstractItemView, QFileDialog, QListWidgetItem)
from PySide2.QtCore import Qt 
from PySide2.QtGui import QTextCursor
import threading
from utils import get_config, env
from .chat_gui import ChatWindow
from backend import process_file
from threading import Thread


class DatabaseChatWindow(ChatWindow):
    def __init__(self, chat_client, chat_thread):
        super().__init__(chat_client, chat_thread)

    def _update_list(self):
        self.database_list.clear()
        # Add items to list from database
        with env.begin() as txn:
            cursor = txn.cursor(db=env.open_db(b"file_database"))
            for key, value in cursor:
                filename = key.decode()
                item = QListWidgetItem(filename, self.database_list)
                item.setFlags(item.flags())

    def setup_ui(self):
        super().setup_ui()

        # Add list of items with checkboxes
        self.database_list = QListWidget()
        self.database_list.setMaximumWidth(200)
        self.database_list.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.database_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.database_list.setSelectionMode(QAbstractItemView.MultiSelection)

        self._update_list()


        list_layout = QVBoxLayout()
        list_layout.addWidget(self.database_list)

        self.process_button = QPushButton("Process")
        self.process_button.clicked.connect(self.handle_process)
        list_layout.addWidget(self.process_button)

        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.handle_delete)
        list_layout.addWidget(self.delete_button)
        

        # Create a QHBoxLayout to hold the database list and add it to the main QVBoxLayout
        layout = QHBoxLayout()

        layout.addWidget(self.central_widget)
        layout.addLayout(list_layout)

        self.central_widget = QWidget()
        self.central_widget.setStyleSheet(f"font-size: {get_config('settings', 'font_size')}pt")

        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

    def handle_process(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file_path:
            process_file(file_path)
            self._update_list()

    def handle_delete(self):
        pass