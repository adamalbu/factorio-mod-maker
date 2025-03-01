import pathlib

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem


class FileTree(QTreeWidget):
    def __init__(self, root_path, name):
        super().__init__()

        self.root_path = pathlib.Path(root_path)
        self.name = name

        self.double_click_connection = None

        self.setColumnCount(1)
        self.setHeaderLabels(['Project'])

        self.create_filetree()

        self.itemDoubleClicked.connect(self.on_item_double_clicked)

    def create_filetree(self):
        for file in self.root_path.iterdir():
            item = self.create_item(file)
            self.addTopLevelItem(item)

    def create_child_items(self, parent_item, file_path):
        for file in file_path.iterdir():
            item = self.create_item(file)
            parent_item.addChild(item)

    def create_item(self, file):
        item = QTreeWidgetItem()
        item.setText(0, file.name)
        item.setData(0, Qt.UserRole, str(file))  # Set the file path as user data
        scale = 32
        if file.is_dir():
            icon = QIcon('icons/folder.png')
            pixmap = icon.pixmap(QSize(scale, scale)).scaled(QSize(scale, scale), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            item.setIcon(0, QIcon(pixmap))
            self.create_child_items(item, file)
        else:
            icon = QIcon('icons/document.png')
            pixmap = icon.pixmap(QSize(scale, scale)).scaled(QSize(scale, scale), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            item.setIcon(0, QIcon(pixmap))
        return item

    @staticmethod
    def on_item_double_clicked(item, column):
        file_path = item.data(0, Qt.UserRole)
        file_path = pathlib.Path(file_path)

        if not file_path.is_dir():
            item.treeWidget().double_click_connection(file_path)

    def connect_double_click(self, function):
        self.double_click_connection = function