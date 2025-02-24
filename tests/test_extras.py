import unittest
import os
import json
from unittest.mock import patch, mock_open
from extras import ConfigFile, AutoUpdateList

class TestConfigFile(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open, read_data='{"key": "value"}')
    @patch('os.path.exists', return_value=True)
    def setUp(self, mock_exists, mock_open):
        self.config = ConfigFile('config.json')

    @patch('builtins.open', new_callable=mock_open, read_data='{"key": "value"}')
    def test_load_from_file(self, mock_open):
        self.config._load_from_file()
        self.assertEqual(self.config['key'], 'value')

    @patch('builtins.open', new_callable=mock_open)
    def test_update_file(self, mock_open):
        self.config['new_key'] = 'new_value'
        mock_open.assert_called_with('config.json', 'w')
        handle = mock_open()
        written_data = ''.join(call[0][0] for call in handle.write.call_args_list)
        expected_data = '{\n    "key": "value",\n    "new_key": "new_value"\n}'
        self.assertEqual(written_data, expected_data)

    def test_auto_update_list(self):
        self.config['list_key'] = ['item1', 'item2']
        self.assertIsInstance(self.config['list_key'], AutoUpdateList)
        self.config['list_key'].append('item3')
        self.assertEqual(self.config['list_key'], ['item1', 'item2', 'item3'])

class TestAutoUpdateList(unittest.TestCase):
    def setUp(self):
        self.parent_config = ConfigFile('config.json')
        self.parent_config['list_key'] = []
        self.auto_update_list = AutoUpdateList(parent_config=self.parent_config, key='list_key')

    def test_append(self):
        self.auto_update_list.append('item1')
        self.assertEqual(self.auto_update_list, ['item1'])
        self.assertEqual(self.parent_config['list_key'], ['item1'])

if __name__ == '__main__':
    unittest.main()