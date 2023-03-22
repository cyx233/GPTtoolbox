import configparser
import json
import os
import lmdb

src_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
config_file = os.path.join(src_dir,'config.ini')


def get_config(namespace, key):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config.get(namespace, key)

def init_usage(usage_file, old_path=None):
    config = configparser.ConfigParser()
    config.read(config_file)

    if not os.path.isabs(usage_file):
        usage_file = os.path.normpath(os.path.join(src_dir, usage_file))

    if old_path and not os.path.isabs(old_path):
        old_path = os.path.normpath(os.path.join(src_dir, old_path))

    os.makedirs(os.path.dirname(usage_file), exist_ok=True)
    try:
        with open(old_path) as f:
            usage = json.load(f)
    except:
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
    usage_file = config.get('settings', 'usage_file')
    with open(usage_file) as f:
        usage = json.load(f)

    if model not in usage:
        usage[model] = 0
    usage[model] += increase

    with open(usage_file, "w") as f:
        json.dump(usage, f)
    return usage_file

def init_db_dir():
    config = configparser.ConfigParser()
    config.read(config_file)
    db_dir = config.get('settings', 'db_dir', fallback="db.lmdb")
    if not os.path.isabs(db_dir):
        db_dir = os.path.normpath(os.path.join(src_dir, db_dir))
    os.makedirs(db_dir, exist_ok=True)
    return db_dir

def init_config():
    config = configparser.ConfigParser()
    config.read(config_file)
    save_dir = config.get('settings', 'save_dir')
    usage_file = config.get('settings', 'usage_file')

    config['settings']['save_dir'] = init_saves(save_dir)
    config['settings']['usage_file'] = init_usage(usage_file, usage_file)
    config['settings']['font_size'] = config.get('settings', 'font_size', fallback='18')
    config['settings']['db_dir'] = init_db_dir()
    if 'db_settings' not in config:
        config['db_settings'] = {}
    config['db_settings']['max_dbs'] = config.get('db_settings', 'max_dbs', fallback='10')
    config['db_settings']['map_size'] = config.get('db_settings', 'map_size', fallback='1000000000')
    config['db_settings']['chunk_size'] = config.get('db_settings', 'chunk_size', fallback='2048')
    if 'model' not in config:
        config['model'] = {}
    config['model']['llm'] = config.get('model', 'chunk_size', fallback='gpt-3.5-turbo')
    config['model']['embedding'] = config.get('model', 'chunk_size', fallback='text-embedding-ada-002')

    with open(config_file, "w") as f:
        config.write(f)

init_config()
env = lmdb.open(
    get_config('settings', 'db_dir'), 
    map_size=int(get_config('db_settings', 'map_size')), 
    max_dbs=int(get_config('db_settings', 'max_dbs')))