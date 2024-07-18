import os
from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog, QDialogButtonBox
from icecream import ic

ic.includeContext = True


def validate_factorio_directory(directory, required_folders, required_files):
    if not os.path.isdir(directory):
        directory = os.path.dirname(directory)

    folders_exist = all(os.path.isdir(os.path.join(directory, folder)) for folder in required_folders)
    files_exist = all(os.path.isfile(os.path.join(directory, file)) for file in required_files)

    return folders_exist and files_exist


class LocationSetupDialog:
    def __init__(self, config, update_button_text):
        self.config = config
        self.update_button_text = update_button_text
        self.dialog = uic.loadUi("ui\\location_setup.ui")

        self.validity_labels = {
            self.dialog.dataValidatorLabel: False,
            self.dialog.exeValidatorLabel: False
        }

        self.dialog.dataBrowseButton.clicked.connect(lambda: self.open_folder_dialog(
            os.path.join(os.getenv('APPDATA', ''), 'Factorio'),
            "Factorio Data Folder"
        ))
        self.dialog.exeBrowseButton.clicked.connect(lambda: self.open_file_dialog(
            "C://Program Files//Factorio//bin//x64",
            "Factorio Exe File",
            "Executable Files (*.exe)"
        ))

        self.data_required_folders = ['mods', 'config', 'saves']
        self.data_required_files = ['player-data.json', 'factorio-current.log']
        self.exe_required_folders = []
        self.exe_required_files = ['factorio.exe', 'factorio.pdb', 'ChromaAppInfo.xml']

        self.dialog.buttonBox.accepted.connect(self.on_ok_pressed)
        self.dialog.buttonBox.rejected.connect(self.dialog.reject)
        self.dialog.dataTextEdit.textChanged.connect(lambda: self.update_validation_status(
            self.dialog.dataTextEdit.text(),
            self.dialog.dataValidatorLabel,
            self.data_required_folders,
            self.data_required_files,
        ))

        self.dialog.exeTextEdit.textChanged.connect(lambda: self.update_validation_status(
            self.dialog.exeTextEdit.text(),
            self.dialog.exeValidatorLabel,
            self.exe_required_folders,
            self.exe_required_files,
        ))

    def show_dialog(self):
        self.dialog.setWindowTitle("Location Setup")
        self.dialog.resize(1200, 400)
        self.update_validation_status(self.dialog.dataTextEdit.text(), self.dialog.dataValidatorLabel,
                                      self.data_required_folders, self.data_required_files)
        self.update_validation_status(self.dialog.exeTextEdit.text(), self.dialog.exeValidatorLabel,
                                      self.exe_required_folders, self.exe_required_files)

        self.dialog.show()

    def open_folder_dialog(self, default_dir, title):
        directory = QFileDialog.getExistingDirectory(self.dialog, title, default_dir)
        if directory:
            self.dialog.dataTextEdit.setText(directory)

    def open_file_dialog(self, default_dir, title, file_filter="All Files (*)"):
        file, _ = QFileDialog.getOpenFileName(self.dialog, title, default_dir, file_filter)
        if file:
            self.dialog.exeTextEdit.setText(file)

    def on_ok_pressed(self):
        self.config["factorio_data"] = self.dialog.dataTextEdit.text().strip()
        self.config["factorio_mods"] = os.path.join(self.dialog.dataTextEdit.text().strip(), "mods")
        self.config["factorio_exe"] = self.dialog.exeTextEdit.text().strip()
        self.update_button_text()  # Call the update function here
        self.dialog.accept()

    def update_validation_status(self, directory_to_validate, label, required_folders, required_files):
        ic()
        if directory_to_validate.strip():
            if validate_factorio_directory(directory_to_validate, required_folders, required_files):
                label.setText("Valid Location")
                label.setStyleSheet("color: green;")
                if label in self.validity_labels.keys():
                    self.validity_labels[label] = True
            else:
                label.setText("Invalid Location")
                label.setStyleSheet("color: red;")
                if label in self.validity_labels.keys():
                    self.validity_labels[label] = False
        else:
            label.setText("")
        if all(self.validity_labels.values()):
            self.dialog.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.dialog.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
