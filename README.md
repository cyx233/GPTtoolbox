# GPTtoolbox
Apps with GUI for various models of GPT. Support searching on local database.

## Installation
### Executable files 
Get them in [Release](https://github.com/cyx233/GPTtoolbox/releases/latest)

### Run in console
```bash
sudo apt-get install qtbase5-dev
sudo apt-get install liblmdb-dev
pip install -r requirements.txt
python src/main.py
```

## API key
1. Get Your [Openai API keys](https://platform.openai.com/account/api-keys)
2. Paste it in config 
    ![](demo/config.png)

**Important Action: Ensure the safety of your API keys. Never make them publicly accessible or upload them to a public repository.**

## Usage
### Available programs
|Name|Filename|Fucntion|
|--|--|--|
|Chat|src/app/stream_chat.py| Text conversation|
|Chat On DB|src/app/db_chat.py| Text conversation according to background knowledge|

### Chat on DB
![](demo/db_chat.png)

Use `Process` to load documents to `LMDB`.  Support text and PDF. PDF will be extracted to text automatically.

Click filenames in the right list to set it as background knowledge.
