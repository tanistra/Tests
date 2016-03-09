import os
import json
from attrdict import AttrDict

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'configuration')


def load_configuration_from_file(file_name):
    file_path = os.path.join(CONFIG_PATH, file_name)
    check_if_config_exists(file_path)
    with open(file_path, 'r') as config_file:
        config = json.load(config_file)
    return AttrDict(config)


def check_if_config_exists(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError("Configuration file not found!\n%s" % file_path)
