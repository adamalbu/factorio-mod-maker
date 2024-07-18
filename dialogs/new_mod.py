import os
import re

from PyQt5 import uic
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtWidgets import QDialogButtonBox
from icecream import ic

from extras import ConfigFile, append_and_return

config = ConfigFile('config.json')


class NewModDialog:
    def __init__(self):
        self.dialog = uic.loadUi("ui\\new_mod_dialog.ui")
        self.dialog.v0Box.setValidator(QIntValidator())
        self.dialog.v1Box.setValidator(QIntValidator())
        self.dialog.v2Box.setValidator(QIntValidator())
        self.dialog.fv0Box.setValidator(QIntValidator())
        self.dialog.fv1Box.setValidator(QIntValidator())

        self.mod_names = []

        self.fields = [
            self.dialog.titleLineEdit,
            self.dialog.nameLineEdit,
            self.dialog.authorLineEdit,
            self.dialog.v0Box,
            self.dialog.v1Box,
            self.dialog.v2Box,
            self.dialog.fv0Box,
            self.dialog.fv1Box
        ]

        for field in self.fields:
            field.textChanged.connect(self.check_mandatory_fields)

        self.dialog.nameLineEdit.textChanged.connect(self.check_mod_name_availability)

        self.dialog.titleLineEdit.textChanged.connect(self.update_mod_name)
        self.dialog.nameLineEdit.textChanged.connect(self.fix_mod_name)

        self.dialog.buttonBox.accepted.connect(self.create_mod)

        self.check_mandatory_fields()

    def show_dialog(self):
        self.dialog.setWindowTitle("New Mod")
        self.dialog.resize(900, 800)

        mod_dirs = list(os.scandir(os.path.join(config["factorio_data"], "mods")))
        pattern = r"(_\d+\.\d+\.\d+)?(\.zip)?$"
        for mod in mod_dirs:
            mod_name = str(mod.name).lower()
            stripped_name = re.sub(pattern, "", mod_name)
            self.mod_names.append(stripped_name)
        self.dialog.show()

    def update_mod_name(self):
        def format_title_text(text):
            # Convert to lowercase, replace spaces with dashes, and remove non-alphanumeric characters except dashes
            # and underscores
            formatted_text = re.sub(r'[^a-z0-9-_]+', '', text.lower().replace(' ', '-'))
            return formatted_text

        # Set the formatted text to nameLineEdit
        self.dialog.nameLineEdit.setText(format_title_text(self.dialog.titleLineEdit.text()))

    def fix_mod_name(self):
        def handle_text_change(text):
            # Replace spaces with dashes
            modified_text = text.replace(' ', '-')
            # Update the text in nameLineEdit
            self.dialog.nameLineEdit.setText(modified_text)

        # Connect the textChanged signal of nameLineEdit to the handle_text_change function
        self.dialog.nameLineEdit.textChanged.connect(handle_text_change)

        # Set validator to allow alphanumeric characters, dashes, and underscores
        pattern = QRegExp("[a-zA-Z0-9_-\\s]+")  # Alphanumeric characters, dashes, and underscores
        validator = QRegExpValidator(pattern)
        self.dialog.nameLineEdit.setValidator(validator)

    def check_mod_name_availability(self):
        mod_name = self.dialog.nameLineEdit.text()
        if mod_name in self.mod_names:
            self.dialog.availabilityLabel.setText("The mod name is already taken.")
            self.dialog.availabilityLabel.setStyleSheet("color: red;")
        else:
            self.dialog.availabilityLabel.setText("The mod name is available.")
            self.dialog.availabilityLabel.setStyleSheet("color: green;")

    def check_mandatory_fields(self):
        all_filled = all(field.text().strip() != "" for field in self.fields)
        self.dialog.buttonBox.button(QDialogButtonBox.Ok).setEnabled(all_filled)

    def create_mod(self):
        name = self.dialog.nameLineEdit.text()
        config["projects"].append(name)
        os.mkdir(os.path.join(config["factorio_data"], "mods"))
