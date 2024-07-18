import json
import os


import os
import json

import os
import json

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

    def _update_nested_objects(self, key):
        value = self[key]
        if isinstance(value, dict):
            self[key] = ConfigFile(self.config_file, value)
        elif isinstance(value, list):
            self[key] = ConfigList(self.config_file, value)

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

    def append_to_list(self, key, item):
        self[key].append(item)
        self._update_file()

class ConfigList(list):
    def __init__(self, config_file, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_file = config_file

    def _update_file(self):
        with open(self.config_file, 'w') as file:
            json.dump(self, file, indent=4)

    def append(self, item):
        super().append(item)
        self._update_file()

    def extend(self, items):
        super().extend(items)
        self._update_file()

    def insert(self, index, item):
        super().insert(index, item)
        self._update_file()

    def remove(self, item):
        super().remove(item)
        self._update_file()

    def pop(self, index=-1):
        result = super().pop(index)
        self._update_file()
        return result

    def clear(self):
        super().clear()
        self._update_file()

    def __setitem__(self, index, value):
        super().__setitem__(index, value)
        self._update_file()

    def __delitem__(self, index):
        super().__delitem__(index)
        self._update_file()

    def __iadd__(self, other):
        super().__iadd__(other)
        self._update_file()

    def __imul__(self, other):
        super().__imul__(other)
        self._update_file()

    def reverse(self):
        super().reverse()
        self._update_file()

    def sort(self, *args, **kwargs):
        super().sort(*args, **kwargs)
        self._update_file()


def append_and_return(lst, item):
    lst.append(item)
    return lst