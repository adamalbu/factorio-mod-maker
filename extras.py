import os
import json

class ConfigFile(dict):
    def __init__(self, config_file, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_file = config_file
        self._load_from_file()

    def _load_from_file(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as file:
                data = json.load(file)
                self.update(data)

    def _update_file(self):
        with open(self.config_file, 'w') as file:
            json.dump(self, file, indent=4)

    def __getitem__(self, key):
        value = super().__getitem__(key)
        if isinstance(value, list):
            return AutoUpdateList(value, parent_config=self, key=key, update_callback=self._update_file)
        return value

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self._update_file()

    def __delitem__(self, key):
        super().__delitem__(key)
        self._update_file()

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self._update_file()

    def clear(self):
        super().clear()
        self._update_file()

    def pop(self, *args):
        result = super().pop(*args)
        self._update_file()
        return result

    def popitem(self):
        result = super().popitem()
        self._update_file()
        return result

    def setdefault(self, *args):
        result = super().setdefault(*args)
        self._update_file()
        return result

class AutoUpdateList(list):
    def __init__(self, initial_list=None, parent_config=None, key=None, update_callback=None):
        if initial_list is None:
            initial_list = []
        super().__init__(initial_list)
        self._parent_config = parent_config
        self._key = key
        self._update_callback = update_callback

    def append(self, item):
        super().append(item)
        self._parent_config[self._key] = self[:]  # Update the list in parent_config
        if self._update_callback:
            self._update_callback()

# Example usage:
config = ConfigFile('config.json')
config['my_list'] = []  # Initialize 'my_list' as an empty list

# Append items to 'my_list' using the desired format
config['my_list'].append('item1')
config['my_list'].append('item2')

# Now 'config.json' will be updated with ['item1', 'item2'] in 'my_list'
