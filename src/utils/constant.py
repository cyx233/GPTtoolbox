import os
import json
from dotenv import load_dotenv

load_dotenv()


API_KEY = os.environ.get('API_KEY')
DATABASE_URL = os.environ.get('DATABASE_URL')

src_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
save_dir = os.path.normpath(os.path.join(src_dir, "../saves"))

usage_file = os.path.join(src_dir,"usage.json")
keyfile = os.path.join(src_dir, "apikey")

if not os.path.exists(usage_file):
    with open(usage_file,"w") as f:
        json.dump({}, f)
os.makedirs(save_dir,exist_ok=True)