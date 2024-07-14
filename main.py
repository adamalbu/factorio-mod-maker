import os
import sys
from PyQt5 import QtWidgets, uic
from icecream import ic

from dev_options_handling import handle_all, handle_reset_factorio_path_on_load
from dialogs.location_setup import LocationSetupDialog
from extras import ConfigFile

config = ConfigFile('config.json')
handle_all()

app = QtWidgets.QApplication(sys.argv)

window = uic.loadUi("ui\\mainwindow.ui")


def update_button_text():
    if config["factorio_path"] is None:
        window.mainButton.setText("Setup")
    else:
        window.mainButton.setText("New Project")


def on_main_button_clicked():
    if config["factorio_path"] is None:
        location_setup_dialog.show_dialog()
    else:
        # Handle other actions when mainButton is clicked
        pass


location_setup_dialog = LocationSetupDialog(config, update_button_text)

window.mainButton.clicked.connect(on_main_button_clicked)
window.showEvent = lambda event: update_button_text()

window.resize(800, 600)  # Set initial window size without changing position

window.show()
update_button_text()
ic(config["factorio_path"])

sys.exit(app.exec_())
