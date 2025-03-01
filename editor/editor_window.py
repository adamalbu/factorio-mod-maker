import json
import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QSplitter, QPushButton, QApplication
import PyQt5.QtWidgets as QtWidgets
import sys


from config import ConfigFile
from editor.file_tree import FileTree
from monaco import MonacoWidget

class Editor(QMainWindow):
    def __init__(self, config_file, mod_path):
        super().__init__()
        self.config = config_file
        self.mod_path = mod_path

        self.setWindowTitle("Mod Editor")
        self.resize(800, 500)

        self.create_ui()

        self.show()

    def create_ui(self):
        layout = QSplitter()
        layout.setOrientation(Qt.Horizontal)

        file_tree = FileTree(self.mod_path, "Factorio")
        file_tree.connect_double_click(self.open_file)

        self.monaco_editor = MonacoWidget()
        self.monaco_editor.setLanguage("json")
        self.monaco_editor.setTheme("vs-dark")

        layout.addWidget(file_tree)
        layout.addWidget(self.monaco_editor)

        self.setCentralWidget(layout)


    def open_file(self, file_path):
        with open(file_path) as f:
            data = f.read()
            self.monaco_editor.setText(data)


def open_editor(location):
    app = QApplication(sys.argv)

    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"

    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    app.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    config = ConfigFile('config.json')

    editor = Editor(config, location)
    # sys.exit(app.exec_())

if __name__ == "__main__":
    config = ConfigFile('config.json')
    open_editor(config.config['setup_data_location'] + '/FMM-first-mod')