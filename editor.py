import sys

from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from config import ConfigFile


class EditorWindow:
    def __init__(self, config, project_path):
        self.config = config
        self.project_path = project_path
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = uic.loadUi("ui/editor_window.ui")

    def open_window(self):
        self.window.setWindowTitle("Factorio Mod Maker")
        self.window.resize(1920, 1080)

        self.window.treeView.doubleClicked.connect(self.item_doubleclicked)

        model = QStandardItemModel()
        project_name = self.project_path.split("/")[-1]
        model.setHorizontalHeaderLabels([project_name])
        self.window.treeView.setModel(model)

        model.appendRow(QStandardItem("Hello"))
        model.appendRow(QStandardItem("World"))

        self.window.show()

    def item_doubleclicked(self, index):
        item = self.window.treeView.model().itemFromIndex(index)
        path = []
        while item:
            path.insert(0, item.text())
            item = item.parent()
        full_path = "/".join(path)
        print(full_path)


    def run(self):
        self.open_window()
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    config = ConfigFile("config.json")
    editor = EditorWindow(config, config['last_project'])
    editor.run()