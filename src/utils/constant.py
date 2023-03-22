import os
import json
import configparser

src_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))

# Create a ConfigParser object and read in the configuration file
config = configparser.ConfigParser()
config.read(os.path.join(src_dir,'config.ini'))

api_key = config.get('settings', 'api_key')

save_dir = config.get('settings', 'save_dir')
usage_file = config.get('settings', 'usage_file')

if not os.path.isabs(save_dir):
    save_dir = os.path.normpath(os.path.join(src_dir, save_dir))

if not os.path.isabs(usage_file):
    save_dir = os.path.normpath(os.path.join(src_dir, usage_file))

if not os.path.exists(usage_file):
    with open(usage_file,"w") as f:
        json.dump({}, f)
os.makedirs(save_dir,exist_ok=True)