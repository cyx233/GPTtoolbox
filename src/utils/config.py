import configparser
import json
import os

src_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
config_file = os.path.join(src_dir,'config.ini')

def init_usage(usage_file, old_path=None):
    config = configparser.ConfigParser()
    config.read(config_file)

    if not os.path.isabs(usage_file):
        usage_file = os.path.normpath(os.path.join(src_dir, usage_file))

    if old_path and not os.path.isabs(old_path):
        old_path = os.path.normpath(os.path.join(src_dir, old_path))

    os.makedirs(os.path.dirname(usage_file), exist_ok=True)
    if old_path:
        with open(old_path) as f:
            usage = json.load(f)
    else:
        usage = {}

    with open(usage_file, "w") as f:
        json.dump(usage, f)
    return usage_file

def init_saves(save_dir):
    config = configparser.ConfigParser()
    config.read(config_file)
    save_dir = config.get('settings', 'save_dir')
    if not os.path.isabs(save_dir):
        save_dir = os.path.normpath(os.path.join(src_dir, save_dir))
    os.makedirs(save_dir,exist_ok=True)
    return save_dir

def increase_usage(model, increase):
    config = configparser.ConfigParser()
    config.read(config_file)
    usage_file = config.get('settings')
    with open(usage_file) as f:
        usage = json.load(f)

    if model not in usage:
        usage[model] = 0
    usage[model] += increase

    with open(usage_file, "w") as f:
        json.dump(usage, f)
    return usage_file

def init_config():
    config = configparser.ConfigParser()
    config.read(config_file)
    save_dir = config.get('settings', 'save_dir')
    usage_file = config.get('settings', 'usage_file')

    config['settings']['save_dir'] = init_saves(save_dir)
    config['settings']['usage_file'] = init_usage(usage_file, usage_file)

    with open(config_file, "w") as f:
        config.write(f)

init_config()