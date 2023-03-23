from PySide2.QtWidgets import ( QMainWindow, QWidget, QVBoxLayout, 
                                QHBoxLayout, QPushButton, QDialog, 
                                QLabel, QLineEdit, QMessageBox,
                                QFileDialog)
from utils import config_file, init_saves, init_usage, init_db_dir, env, get_config
import configparser

class DBConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Advanced Database Settings")
        self.setMinimumSize(400, 300)

        layout = QVBoxLayout()

        # Add widgets for database settings
        self.max_dbs_label = QLabel("Maximum Number of Databases:")
        self.max_dbs_edit = QLineEdit()
        self.map_size_label = QLabel("Maximum Database Size (in bytes):")
        self.map_size_edit = QLineEdit()
        self.chunk_size_label = QLabel("Text Chunk Size")
        self.chunk_size_edit = QLineEdit()


        config = configparser.ConfigParser()
        config.read(config_file)

        max_dbs = config.get('db_settings', 'max_dbs')
        map_size = config.get('db_settings', 'map_size')
        chunk_size = config.get('db_settings', 'chunk_size')

        # Add default values to the widgets
        self.max_dbs_edit.setText(str(max_dbs))
        self.map_size_edit.setText(str(map_size))
        self.chunk_size_edit.setText(str(chunk_size))

        # Add widgets to the layout
        layout.addWidget(self.max_dbs_label)
        layout.addWidget(self.max_dbs_edit)
        layout.addWidget(self.map_size_label)
        layout.addWidget(self.map_size_edit)
        layout.addWidget(self.chunk_size_label)
        layout.addWidget(self.chunk_size_edit)

        # Add OK and Cancel buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def accept(self):
        # Get the new values for max_dbs and map_size from the text boxes
        max_dbs = self.max_dbs_edit.text()
        map_size = self.map_size_edit.text()

        config = configparser.ConfigParser()
        config.read(config_file)
        
        if max_dbs and max_dbs.isdigit():
            config['db_settings']['max_dbs'] = int(max_dbs)
        else:
            QMessageBox.warning(self, "Warning", "max_dbs is not a number")
        if map_size and map_size.isdigit():
            config['db_settings']['map_size'] = int(map_size)
        else:
            QMessageBox.warning(self, "Warning", "map_size is not a number")
        if chunk_size and chunk_size.isdigit():
            config['db_settings']['chunk_size'] = int(chunk_size)
        else:
            QMessageBox.warning(self, "Warning", "chunk_size is not a number")

        with open(config_file, "w") as f:
            config.write(f)

        env.set_mapsize(int(map_size))

        # Call the accept method of the dialog to close it
        super().accept()

class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Edit Config")
        self.setMinimumSize(600, 400)

        layout = QVBoxLayout()

        self.api_key_label = QLabel("API Key:")
        self.save_dir_label = QLabel("Saves Location")
        self.usage_file_label = QLabel("Usage Record")
        self.db_dir_lable = QLabel("Database Directory")
        self.font_size_lable = QLabel("Font Size")
        labels = [
            self.api_key_label,
            self.save_dir_label,
            self.usage_file_label,
            self.db_dir_lable,
            self.font_size_lable,
        ]

        self.api_key_edit = QLineEdit()
        self.save_dir_edit = QLineEdit()
        self.usage_file_edit = QLineEdit()
        self.db_dir_edit = QLineEdit()
        self.font_size_edit = QLineEdit()

        edits = [
            self.api_key_edit,
            self.save_dir_edit,
            self.usage_file_edit,
            self.db_dir_edit,
            self.font_size_edit,
        ]

        for label, edit in zip(labels, edits):
            hbox = QHBoxLayout()
            hbox.addWidget(label)
            hbox.addWidget(edit)

            if label in [self.save_dir_label, self.usage_file_label, self.db_dir_lable]:
                button = QPushButton("Browse")
                if label == self.save_dir_label:
                    button.clicked.connect(self.select_save_dir)
                elif label == self.usage_file_label:
                    button.clicked.connect(self.select_usage_file)
                else:
                    button.clicked.connect(self.select_db_dir)
                hbox.addWidget(button)
            layout.addLayout(hbox)
        


        # Load the current API key from config.ini

        config = configparser.ConfigParser()
        config.read(config_file)

        api_key = config.get('settings','api_key')
        save_dir = config.get('settings','save_dir')
        usage_file = config.get('settings','usage_file')
        db_dir = config.get('settings','db_dir')
        font_size = config.get('settings','font_size')

        self.old_path = usage_file
        self.api_key_edit.setText(api_key)
        self.save_dir_edit.setText(save_dir)
        self.usage_file_edit.setText(usage_file)
        self.db_dir_edit.setText(db_dir)
        self.font_size_edit.setText(font_size)
        self.setStyleSheet(f"font-size: {font_size}pt")

        button_layout = QHBoxLayout()

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.accept)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)

        db_config_button = QPushButton("Advanced Database Settings")
        db_config_button.clicked.connect(self.show_db_config_dialog)

        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(db_config_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def accept(self):
        # Save the API key to config.ini
        api_key = self.api_key_edit.text().strip()
        save_dir = self.save_dir_edit.text().strip()
        usage_file = self.usage_file_edit.text().strip()
        db_dir = self.db_dir_edit.text().strip()
        font_size = self.font_size_edit.text().strip()


        config = configparser.ConfigParser()
        config.read(config_file)

        if api_key:
            config['settings']['api_key'] = api_key
        else:
            QMessageBox.warning(self, "Warning", "API Key cannot be empty")

        config['settings']['save_dir'] = save_dir
        init_saves(save_dir)

        config['settings']['usage_file'] = usage_file
        init_usage(usage_file, self.old_path)

        config['settings']['db_dir'] = db_dir
        init_db_dir()

        config['settings']['font_size'] = font_size
        self.setStyleSheet(f"font-size: {font_size}pt")

        with open(config_file, "w") as f:
            config.write(f)
        super().accept()

    def select_save_dir(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self, "Select Directory", self.save_dir_edit.text(), options=options)
        if directory:
            self.save_dir_edit.setText(directory)

    def select_usage_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Select File", self.usage_file_edit.text(), "JSON Files (*.json)", options=options)
        if file_path:
            self.usage_file_edit.setText(file_path)

    def select_db_dir(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self, "Select Directory", self.db_dir_edit.text(), options=options)
        if directory:
            self.db_dir_edit.setText(directory)

    def show_db_config_dialog(self):
        # Show the advanced database settings dialog
        db_settings_dialog = DBConfigDialog(parent=self)
        db_settings_dialog.exec_()