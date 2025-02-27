import json

class ConfigFile:
    def __init__(self, file_path):
        self.file_path = file_path
        self.config = self.load_config()

    def load_config(self):
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            with open(self.file_path, 'w') as file:
                json.dump({}, file)

    def save_config(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.config, file, indent=4)
