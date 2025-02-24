import unittest
from unittest.mock import MagicMock, patch, call
from main import MainWindow
from extras import ConfigFile

class TestMainWindow(unittest.TestCase):
    @patch('main.QtWidgets.QApplication')
    @patch('main.uic.loadUi')
    def setUp(self, mock_loadUi, mock_QApplication):
        self.config = ConfigFile('config.json')
        self.config['factorio_data'] = None
        self.config['projects'] = ['Project1', 'Project2']
        self.main_window = MainWindow(self.config)
        self.main_window.window = MagicMock()

    def test_update_button_text_setup(self):
        self.config['factorio_data'] = None
        self.main_window.update_button_text()
        self.main_window.window.mainButton.setText.assert_called_with('Setup')

    def test_update_button_text_new_project(self):
        self.config['factorio_data'] = 'some_data'
        self.main_window.update_button_text()
        self.main_window.window.mainButton.setText.assert_called_with('New Project')

    def test_on_main_button_clicked_setup(self):
        self.config['factorio_data'] = None
        self.main_window.location_setup_dialog.show_dialog = MagicMock()
        self.main_window.on_main_button_clicked()
        self.main_window.location_setup_dialog.show_dialog.assert_called_once()

    def test_on_main_button_clicked_new_project(self):
        self.config['factorio_data'] = 'some_data'
        self.main_window.new_mod_dialog.show_dialog = MagicMock()
        self.main_window.on_main_button_clicked()
        self.main_window.new_mod_dialog.show_dialog.assert_called_once()

if __name__ == '__main__':
    unittest.main()