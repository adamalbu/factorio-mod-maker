import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QSpacerItem

from dialogs.location_validator import LocationSetup

from config import ConfigFile


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
        print("New Mod Setup") # TODO: Implement this


if __name__ == "__main__":
    config = ConfigFile('config.json')

    app = QtWidgets.QApplication(sys.argv)

    main_window = WelcomeScreen(config)
    main_window.create_ui()
    main_window.show()
    main_window.open_location_setup()  # FIXME: Remove this line

    app.exec()
