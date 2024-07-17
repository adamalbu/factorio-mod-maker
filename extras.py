import json
import os


class ConfigFile(dict):
    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_file = config
        self._load_from_file()

    def _load_from_file(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as file:
                data = json.load(file)
                self.update(data)

    def _update_file(self):
        with open(self.config_file, 'w') as file:
            json.dump(self, file, indent=4)

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
