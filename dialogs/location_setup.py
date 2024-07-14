import os
from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog, QDialogButtonBox

class LocationSetupDialog:
    def __init__(self, config, update_button_text):
        self.config = config
        self.update_button_text = update_button_text
        self.dialog = uic.loadUi("ui\\location_setup.ui")
        self.dialog.browseButton.clicked.connect(self.open_file_dialog)
        self.dialog.buttonBox.accepted.connect(self.on_ok_pressed)
        self.dialog.buttonBox.rejected.connect(self.dialog.reject)
        self.dialog.locationTextEdit.textChanged.connect(self.update_validation_status)

    def show_dialog(self):
        self.dialog.setWindowTitle("Location Setup")
        self.update_validation_status(self.dialog.locationTextEdit.text())
        self.dialog.show()

    def open_file_dialog(self):
        default_dir = os.path.join(os.getenv('APPDATA', ''), 'Factorio')
        directory = QFileDialog.getExistingDirectory(self.dialog, "Select Factorio Path", default_dir)
        if directory:
            self.update_ui_with_path(directory)

    def update_ui_with_path(self, directory):
        self.dialog.locationTextEdit.setText(directory)
        self.update_validation_status(self.dialog.locationTextEdit.text())

    def on_ok_pressed(self):
        directory = self.dialog.locationTextEdit.text().strip()
        if self.validate_factorio_directory(directory):
            self.config["factorio_path"] = directory
            self.update_button_text()  # Call the update function here
            self.dialog.accept()
        else:
            # Optionally display an error message or handle invalid input
            pass

    def update_validation_status(self, text):
        if text.strip():
            if self.validate_factorio_directory(text):
                self.dialog.locationValidatorLabel.setText("Valid Location")
                self.dialog.locationValidatorLabel.setStyleSheet("color: green;")
                self.dialog.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
            else:
                self.dialog.locationValidatorLabel.setText("Invalid Location")
                self.dialog.locationValidatorLabel.setStyleSheet("color: red;")
                self.dialog.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        else:
            self.dialog.locationValidatorLabel.setText("")
            self.dialog.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

    def validate_factorio_directory(self, directory):
        required_folders = ['mods', 'config', 'saves']
        required_files = ['player-data.json', 'factorio-current.log']
        folders_exist = all(os.path.isdir(os.path.join(directory, folder)) for folder in required_folders)
        files_exist = all(os.path.isfile(os.path.join(directory, file)) for file in required_files)
        return folders_exist and files_exist
