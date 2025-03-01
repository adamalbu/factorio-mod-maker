import os.path

from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QWidget, QVBoxLayout


class MonacoEditorWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Create QVBoxLayout to manage widget layout
        layout = QVBoxLayout(self)

        # Create a QWebEngineView widget to load Monaco Editor
        self.view = QWebEngineView(self)

        # Load the Monaco HTML file (ensure the path is correct)
        path = os.path.abspath('monaco_editor/index.html')
        self.view.setUrl(QUrl.fromLocalFile(path))

        # Add the QWebEngineView to the layout
        layout.addWidget(self.view)

        # Set layout for the widget
        self.setLayout(layout)
        self.setWindowTitle("Monaco Editor Widget")
        self.setGeometry(100, 100, 800, 600)