import sys, os
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog

from dev_options_handling import handle_all
from dialogs.location_setup import LocationSetupDialog
from dialogs.new_mod import NewModDialog
from extras import ConfigFile

from editor import EditorWindow

class MainWindow:
    def __init__(self, config):
        self.config = config
        self.app = QtWidgets.QApplication(sys.argv)
        if self.config['last_project']:
            self.start_editor()
            return

        self.window = uic.loadUi('ui\\mainwindow.ui')
        self.location_setup_dialog = LocationSetupDialog(config, self.update_button_text)
        self.new_mod_dialog = NewModDialog()

        self.setup_ui()
        self.update_button_text()

    def setup_ui(self):
        self.window.actionNew.triggered.connect(self.new_mod_dialog.show_dialog)
        self.window.actionOpen.triggered.connect(self.open_project_picker)

        self.window.mainButton.clicked.connect(self.on_main_button_clicked)
        self.window.showEvent = lambda event: self.update_button_text()

        self.window.setWindowTitle("Factorio Mod Maker")
        self.window.resize(1000, 600)
        self.window.show()

    def open_project_picker(self):
        options = QFileDialog.Options()
        default_dir = os.path.join(os.getenv('APPDATA', ''), 'factorio', 'mods')
        folder_name = QFileDialog.getExistingDirectory(self.window, "Select Folder", default_dir, options=options)
        if folder_name:
            self.config['last_project'] = folder_name
            self.start_editor()

    def start_editor(self):
        self.window.close()

        editor = EditorWindow(self.config, self.config['last_project'])
        editor.open_window()

    def update_button_text(self):
        if self.config['factorio_data'] is None:
            self.window.mainButton.setText('Setup')
        else:
            self.window.mainButton.setText('New Project')

    def on_main_button_clicked(self):
        if self.config['factorio_data'] is None:
            self.location_setup_dialog.show_dialog()
        else:
            self.new_mod_dialog.show_dialog()

    def run(self):
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    config = ConfigFile('config.json')
    handle_all()
    main_window = MainWindow(config)
    main_window.run()