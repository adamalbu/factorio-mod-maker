import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QAction

from dev_options_handling import handle_all
from dialogs.location_setup import LocationSetupDialog
from dialogs.new_mod import NewModDialog
from extras import ConfigFile

config = ConfigFile('config.json')
handle_all()

app = QtWidgets.QApplication(sys.argv)

window = uic.loadUi('ui\\mainwindow.ui')

def update_button_text():
    if config['factorio_data'] is None:
        window.mainButton.setText('Setup')
    else:
        window.mainButton.setText('New Project')


def on_main_button_clicked():
    if config['factorio_data'] is None:
        location_setup_dialog.show_dialog()
    else:
        new_mod_dialog.show_dialog()


location_setup_dialog = LocationSetupDialog(config, update_button_text)
new_mod_dialog = NewModDialog()

# region Menu actions
window.actionNew.triggered.connect(new_mod_dialog.show_dialog)
for project in config['projects']:
    project = QAction(project)
    # window.menubar.addAction(project)
    window.menu_Open.addAction(project)
# window.menu_Open.addAction(QAction("test"))
# ic(window.menu_Open)
# endregion

window.mainButton.clicked.connect(on_main_button_clicked)
window.showEvent = lambda event: update_button_text()

window.setWindowTitle("Factorio Mod Maker")
window.resize(1000, 600)
window.show()
update_button_text()

sys.exit(app.exec_())
