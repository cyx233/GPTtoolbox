import sys
from PySide2.QtWidgets import ( QApplication, QMainWindow, QWidget, 
                                QVBoxLayout, QHBoxLayout, QPushButton, 
                                QDialog, QLabel, QLineEdit, QMessageBox,
                                QFileDialog)
from PySide2.QtCore import Qt, QSettings
from app import stream_chat
from utils import config_file, init_saves, init_usage

from .chat_gui import ChatWindow

class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Edit Config")
        self.setMinimumSize(600, 400)

        layout = QVBoxLayout()

        self.api_key_label = QLabel("API Key:")
        self.save_dir_label = QLabel("Saves Location")
        self.usage_file_label = QLabel("Usage Record")
        self.font_size_lable = QLabel("Font Size")
        labels = [
            self.api_key_label,
            self.save_dir_label,
            self.usage_file_label,
            self.font_size_lable
        ]

        self.api_key_edit = QLineEdit()
        self.save_dir_edit = QLineEdit()
        self.usage_file_edit = QLineEdit()
        self.font_size_edit = QLineEdit()

        edits = [
            self.api_key_edit,
            self.save_dir_edit,
            self.usage_file_edit,
            self.font_size_edit,
        ]

        for label, edit in zip(labels, edits):
            hbox = QHBoxLayout()
            hbox.addWidget(label)
            hbox.addWidget(edit)

            if label == self.save_dir_label or label == self.usage_file_label:
                button = QPushButton("Browse")
                if label == self.save_dir_label:
                    button.clicked.connect(self.select_save_dir)
                else:
                    button.clicked.connect(self.select_usage_file)
                hbox.addWidget(button)

            layout.addLayout(hbox)
        

        # Load the current API key from config.ini
        settings = QSettings(config_file, QSettings.IniFormat)
        api_key = settings.value("settings/api_key", "")
        save_dir = settings.value("settings/save_dir", "save_dir")
        usage_file = settings.value("settings/usage_file", "usage_file")
        font_size = settings.value("settings/font_size", "18")

        self.old_path = usage_file
        self.api_key_edit.setText(api_key)
        self.save_dir_edit.setText(save_dir)
        self.usage_file_edit.setText(usage_file)
        self.font_size_edit.setText(font_size)
        self.setStyleSheet(f"font-size: {font_size}pt")

        button_layout = QHBoxLayout()

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def accept(self):
        # Save the API key to config.ini
        api_key = self.api_key_edit.text().strip()
        save_dir = self.save_dir_edit.text().strip()
        usage_file = self.usage_file_edit.text().strip()
        font_size = self.font_size_edit.text().strip()
        settings = QSettings(config_file, QSettings.IniFormat)

        if api_key:
            settings.setValue("settings/api_key", api_key)
        else:
            QMessageBox.warning(self, "Warning", "API Key cannot be empty")

        settings.setValue("settings/save_dir", save_dir)
        init_saves(save_dir)

        settings = QSettings(config_file, QSettings.IniFormat)
        settings.setValue("settings/usage_file", usage_file)
        init_usage(usage_file, self.old_path)

        settings.setValue("settings/font_size", font_size)
        self.setStyleSheet(f"font-size: {font_size}pt")
        super().accept()

    def select_save_dir(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self, "Select Directory", self.save_dir_edit.text(), options=options)
        if directory:
            self.save_dir_edit.setText(directory)

    def select_usage_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getSaveFileName(self, "Select File", self.usage_file_edit.text(), "JSON Files (*.json)", options=options)
        if file_path:
            self.usage_file_edit.setText(file_path)

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

        config_button = QPushButton("Config")
        config_button.clicked.connect(self.show_config_dialog)

        layout.addWidget(chat_button)
        layout.addWidget(config_button)

        settings = QSettings(config_file, QSettings.IniFormat)

        # Add buttons for other programs here
        self.central_widget.setLayout(layout)
        self.central_widget.setStyleSheet(f"font-size: {settings.value('settings/font_size', '18')}pt")
    
    def launch_stream_chat(self):
        stream_chat()

    def show_config_dialog(self):
        dialog = ConfigDialog(parent=self)
        if dialog.exec_() == QDialog.Accepted:
            QMessageBox.information(self, "Information", "Config saved. Some settings require reloading.")