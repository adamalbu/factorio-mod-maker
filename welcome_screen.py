import os
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QSpacerItem

from dialogs.location_validator import LocationSetup
from editor.editor_window import Editor
from config import ConfigFile
from dialogs.new_mod import NewModDialog

class WelcomeScreen(QMainWindow):
    def __init__(self, config_file):
        super().__init__()
        self.config = config_file
        self.set_up_window()
        self.create_ui()

    def set_up_window(self):
        self.setWindowTitle("Factorio Mod Maker")
        self.resize(500, 300)

    def create_ui(self):
        layout = QVBoxLayout()

        setup_button = QPushButton("&Setup Factorio Location")
        setup_button.clicked.connect(self.open_location_setup)

        new_mod_button = QPushButton("&Create New Mod")
        new_mod_button.clicked.connect(self.open_new_mod_setup)

        spacer = QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        layout.addItem(spacer)
        layout.addWidget(setup_button)
        layout.addWidget(new_mod_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def open_location_setup(self):
        location_setup = LocationSetup(self.config)
        location_setup.exec_()

    def open_new_mod_setup(self):
        new_mod_setup = NewModDialog(self.config)
        accepted = new_mod_setup.exec_()
        if accepted == 1:
            self.open_editor()

    def open_editor(self):
        self.hide()  # Hide the Welcome Screen
        open_editor(self.config)  # Pass config to the editor

def open_editor(config):
    last_project_name = config.config['last_project']
    last_project_path = os.path.join(config.config['setup_data_location'], last_project_name)

    editor = Editor(config, last_project_path)
    editor.create_ui()
    editor.show()

if __name__ == "__main__":
    # Set up the environment variables for high-DPI scaling
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"

    # Initialize the application with high-DPI scaling enabled
    app = QtWidgets.QApplication(sys.argv)

    # Enable High DPI scaling across the application
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    app.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    # Proceed with the rest of the program
    config = ConfigFile('config.json')
    main_window = WelcomeScreen(config)
    main_window.create_ui()
    main_window.show()

    # Start the event loop
    sys.exit(app.exec_())
