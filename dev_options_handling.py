from icecream import ic

from extras import ConfigFile

config = ConfigFile('config.json')

def handle_all():
    ic()
    handle_reset_factorio_path_on_load()
    handle_ic_debugger()

def config_option_handler(func):
    def wrapper():
        option_key = func.__name__.replace("handle_", "")  # Remove "handle_" prefix from function name
        if config["dev_options"].get(option_key, False):
            func()
    return wrapper

@config_option_handler
def handle_reset_factorio_path_on_load():
    ic(config["factorio_path"])
    config["factorio_path"] = None
    ic(config["factorio_path"])

@config_option_handler
def handle_ic_debugger():
    ic.enable()
