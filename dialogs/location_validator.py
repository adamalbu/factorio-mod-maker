from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QFileDialog, QSpacerItem, \
    QDialogButtonBox
from PyQt5 import QtWidgets

from icecream import ic
import os

class ValidatorWidget(QVBoxLayout):
    def __init__(self, label, valid_files, valid_folders, default_path):
        super().__init__()
        self.valid_files = valid_files
        self.valid_folders = valid_folders
        self.default_path = default_path
        self.location = ""
        self.valid = False

        self.validate_connect_func = None

        label = QLabel(label)

        self.path = QLineEdit()
        self.path.textChanged.connect(lambda: self.validate_from_textbox(self.path.text()))
        self.browse = QPushButton("Browse")
        self.browse.clicked.connect(self.browse_and_validate)
        self.status = QLabel("Invalid Location")
        self.status.setStyleSheet("color: red")

        self.addWidget(label)
        h_box = QHBoxLayout()
        h_box.addWidget(self.path)
        h_box.addWidget(self.browse)
        self.addLayout(h_box)
        self.addWidget(self.status)

    def connect_validate(self, func):
        self.validate_connect_func = func

    def open_folder_picker(self):
        file_dialog = QFileDialog()
        folder_path = file_dialog.getExistingDirectory(file_dialog, "Select Folder", self.default_path)
        return folder_path

    def open_file_picker(self):
        file_dialog = QFileDialog()
        file_path = file_dialog.getOpenFileName(self, "Select File", self.default_path)
        return file_path

    def validate(self):
        valid_files = all(os.path.isfile(os.path.join(self.location, file)) \
                          for file in self.valid_files)
        valid_folders = all(os.path.isdir(os.path.join(self.location, folder)) \
                            for folder in self.valid_folders)

        valid = valid_files and valid_folders
        self.valid = valid

        if self.validate_connect_func:
            self.validate_connect_func(valid)

        return valid

    def update_status(self, valid):
        if valid:
            self.status.setText("Valid Location")
            self.status.setStyleSheet("color: green")
        else:
            self.status.setText("Invalid Location")
            self.status.setStyleSheet("color: red")

    def validate_from_textbox(self, path):
        self.location = path
        valid = self.validate()
        self.update_status(valid)

    def browse_and_validate(self):
        self.location = self.open_folder_picker() # TODO: should be able to also use file picker
        valid = self.validate()
        self.update_status(valid)
        self.path.setText(self.location)

class LocationSetup(QDialog):
    def __init__(self, config):
        super().__init__()

        self.config = config

        self.dialog_buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.dialog_buttons.button(QDialogButtonBox.Ok).setEnabled(False)
        self.dialog_buttons.accepted.connect(self.save_config)
        self.dialog_buttons.rejected.connect(self.reject)

        self.exe_validation = None
        self.data_validation = None
        self.exe_status: QLabel = QLabel()
        self.exe_path: QLineEdit = QLineEdit()
        self.data_status: QLabel = QLabel()
        self.data_path: QLineEdit = QLineEdit()
        self.data_location = ""
        self.exe_location = ""

        self.set_up_window()
        self.create_ui()

    def save_config(self):
        self.config.config['setup_data_location'] = self.data_validation.location + "/mods"
        self.config.config['setup_exe_location'] = self.exe_validation.location
        self.config.save_config()
        self.accept()

    def set_up_window(self):
        self.setWindowTitle("Factorio Location Setup")
        self.resize(800, 500)

    def validation_update(self, _valid):
        if self.data_validation.valid and self.exe_validation.valid:
            self.dialog_buttons.button(QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.dialog_buttons.button(QDialogButtonBox.Ok).setEnabled(False)

    def create_ui(self):
        layout = QVBoxLayout()

        label = "Factorio Data Location"
        required_folders = ['mods', 'config', 'saves']
        required_files = ['player-data.json', 'factorio-current.log']
        default_location = os.path.join(os.getenv('APPDATA'), 'Factorio')
        self.data_validation = ValidatorWidget(label, required_files, required_folders, default_location)
        self.data_validation.connect_validate(self.validation_update)

        label = "Factorio Executable Location"
        required_folders = []
        required_files = ['factorio.exe']
        default_location = "C:\\Program Files\\Factorio\\bin\\x64"
        self.exe_validation = ValidatorWidget(label, required_files, required_folders, default_location)
        self.exe_validation.connect_validate(self.validation_update)

        layout.addLayout(self.data_validation)
        layout.addLayout(self.exe_validation)

        spacer = QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        layout.addItem(spacer)

        layout.addWidget(self.dialog_buttons)

        self.setLayout(layout)