import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QSpacerItem, QDialog, QLabel, QHBoxLayout

from dev_options_handling import handle_all
from extras import ConfigFile


class WelcomeScreen(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.config = config

        self.set_up_window()
        self.create_ui()

    def set_up_window(self):
        self.setWindowTitle("Factorio Mod Maker")
        self.resize(1000, 600)

    def create_ui(self):
        layout = QVBoxLayout()

        setup_button = QPushButton("Setup Factorio Location")
        setup_button.clicked.connect(self.open_location_setup)

        new_mod_button = QPushButton("Create New Mod")
        new_mod_button.clicked.connect(self.open_new_mod_setup)

        spacer = QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        layout.addItem(spacer)
        layout.addWidget(setup_button)
        layout.addWidget(new_mod_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def open_location_setup(self):
        location_setup = LocationSetup()
        location_setup.exec_()

    def open_new_mod_setup(self):
        print("New Mod Setup")

class LocationSetup(QDialog):
    def __init__(self):
        super().__init__()

        self.set_up_window()
        self.create_ui()

    def set_up_window(self):
        self.setWindowTitle("Factorio Location Setup")
        # self.resize(500, 300)

    def create_ui(self):
        layout = QVBoxLayout()

        data_label = QLabel("Factorio Location:")
        data_layout = QHBoxLayout()
        data_text_edit = QtWidgets.QLineEdit()
        data_browse = QPushButton("Browse")
        data_location_status = QLabel("Invalid Location")
        data_location_status.setStyleSheet("color: red")

        data_layout.addWidget(data_text_edit)
        data_layout.addWidget(data_browse)

        exe_label = QLabel("Factorio Executable:")
        exe_layout = QHBoxLayout()
        exe_text_edit = QtWidgets.QLineEdit()
        exe_browse = QPushButton("Browse")
        exe_location_status = QLabel("Invalid Executable")
        exe_location_status.setStyleSheet("color: red")

        exe_layout.addWidget(exe_text_edit)
        exe_layout.addWidget(exe_browse)

        layout.addWidget(data_label)
        layout.addLayout(data_layout)
        layout.addWidget(data_location_status)
        layout.addWidget(exe_label)
        layout.addLayout(exe_layout)
        layout.addWidget(exe_location_status)


        self.setLayout(layout)

if __name__ == "__main__":
    config = ConfigFile('config.json')
    handle_all()

    app = QtWidgets.QApplication(sys.argv)

    main_window = WelcomeScreen(config)
    main_window.create_ui()
    main_window.show()

    app.exec()
