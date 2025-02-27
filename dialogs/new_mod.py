import os

from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, QLine
from PyQt5.QtGui import QFont, QIntValidator
from PyQt5.QtWidgets import QDialog, QLineEdit, QLabel, QSpacerItem, QFormLayout, QWidget, QFrame, QPushButton, \
    QTextEdit, QHBoxLayout, QDialogButtonBox

from config import ConfigFile


class NewModDialog(QDialog):
    def __init__(self, config_file):
        super().__init__()

        self.config = config_file
        self.list_of_mods = []

        for mod in os.listdir(self.config.config['setup_data_location']):
            self.list_of_mods.append(mod.rstrip('.zip'))

        self.setWindowTitle("New Mod Setup")
        self.resize(800, 500)

        layout = QFormLayout()

        title_label = QLabel("*Mod &Title:")
        self.title = QLineEdit()
        title_label.setBuddy(self.title)
        self.title.textChanged.connect(self.title_updated)
        self.title.setFont(QFont("Courier New", 9))
        layout.addRow(title_label, self.title)

        name_label = QLabel("*Mod &Name:")
        self.name = QLineEdit()
        name_label.setBuddy(self.name)
        self.name.setFont(QFont("Courier New", 9))
        self.name.textChanged.connect(self.name_update)
        layout.addRow(name_label, self.name)
        self.availability = QLabel("Name is available")
        self.availability.setStyleSheet("color: green")
        layout.addRow(QWidget(), self.availability)

        version_label = QLabel("*&Version:")
        version_layout = QHBoxLayout()
        self.v1 = QLineEdit()
        self.v1.setValidator(QIntValidator(0, 65535))
        self.v1.textChanged.connect(self.check_mandatory_fields)
        self.v2 = QLineEdit()
        self.v2.setValidator(QIntValidator(0, 65535))
        self.v2.textChanged.connect(self.check_mandatory_fields)
        self.v3 = QLineEdit()
        self.v3.setValidator(QIntValidator(0, 65535))
        self.v3.textChanged.connect(self.check_mandatory_fields)
        version_layout.addWidget(self.v1)
        version_layout.addWidget(QLabel("."))
        version_layout.addWidget(self.v2)
        version_layout.addWidget(QLabel("."))
        version_layout.addWidget(self.v3)
        version_label.setBuddy(self.v1)
        layout.addRow(version_label, version_layout)

        factorio_version_label = QLabel("*Factorio &Version:")
        factorio_version_layout = QHBoxLayout()
        self.fv1 = QLineEdit()
        self.fv1.setValidator(QIntValidator(0, 65535))
        self.fv1.textChanged.connect(self.check_mandatory_fields)
        self.fv2 = QLineEdit()
        self.fv2.setValidator(QIntValidator(0, 65535))
        self.fv2.textChanged.connect(self.check_mandatory_fields)
        factorio_version_layout.addWidget(self.fv1)
        factorio_version_layout.addWidget(QLabel("."))
        factorio_version_layout.addWidget(self.fv2)
        factorio_version_label.setBuddy(self.fv1)
        layout.addRow(factorio_version_label, factorio_version_layout)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        layout.addRow(separator)

        author_label = QLabel("*&Author:")
        self.author = QLineEdit()
        author_label.setBuddy(self.author)
        self.author.textChanged.connect(self.check_mandatory_fields)
        layout.addRow(author_label, self.author)

        contact_label = QLabel("&Contact:")
        self.contact = QLineEdit()
        contact_label.setBuddy(self.contact)
        layout.addRow(contact_label, self.contact)

        homepage_label = QLabel("&Homepage:")
        self.homepage = QLineEdit()
        homepage_label.setBuddy(self.homepage)
        layout.addRow(homepage_label, self.homepage)

        description_label = QLabel("&Description:")
        self.description = QTextEdit()
        description_label.setBuddy(self.description)
        layout.addRow(description_label, self.description)

        spacer = QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        layout.addItem(spacer)

        self.dialog_buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.dialog_buttons.button(QDialogButtonBox.Ok).setEnabled(False)
        self.dialog_buttons.accepted.connect(self.generate_mod_data)
        self.dialog_buttons.rejected.connect(self.reject)

        layout.addWidget(self.dialog_buttons)

        self.setLayout(layout)

        self.show()

    def title_updated(self):
        self.name.setText(self.title.text())
        self.name_update()

    def name_update(self):
        text = self.name.text()
        name = text.replace(" ", "-")
        # remove everything except alphanumeric characters, dashes and underscores
        name = ''.join(e for e in name if e.isalnum() or e == '-' or e == '_')
        self.name.setText(name)

        name = self.name.text()

        mods_path = self.config.config['setup_data_location']

        if name in self.list_of_mods:
            self.availability.setText("Name is not available")
            self.availability.setStyleSheet("color: red")
        else:
            self.availability.setText("Name is available")
            self.availability.setStyleSheet("color: green")

        self.check_mandatory_fields()

    def check_mandatory_fields(self):
        info = self.title.text() and self.name.text() and self.author.text()
        versions = self.v1.text() and self.v2.text() and self.v3.text() and self.fv1.text() and self.fv2.text()
        valid = (info and versions) != ''

        self.dialog_buttons.button(QDialogButtonBox.Ok).setEnabled(valid)

    def generate_mod_data(self):
        if 'projects' not in self.config.config.keys():
            self.config.config['projects'] = []
        self.config.config['projects'].append(self.name.text())
        self.config.save_config()

        mods_path = self.config.config['setup_data_location']
        os.mkdir(os.path.join(mods_path, self.name.text()))
        info = {
            "name": self.name.text(),
            "title": self.title.text(),
            "version": f"{self.v1.text()}.{self.v2.text()}.{self.v3.text()}",
            "factorio_version": f"{self.fv1.text()}.{self.fv2.text()}",
            "author": self.author.text(),
            "contact": self.contact.text(),
            "homepage": self.homepage.text(),
            "description": self.description.toPlainText()
        }

        with open(os.path.join(mods_path, self.name.text(), "info.json"), 'w') as f:
            f.write(str(info))

        self.config.config['last_project'] = self.name.text()
        self.accept()


if __name__ == "__main__":
    config = ConfigFile('config.json')
    dialog = NewModDialog(config)
    dialog.exec_()