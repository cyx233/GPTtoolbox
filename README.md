# GPTtoolbox
scripts for various models of GPT

## Requirements
```bash
pip install -r requirements.txt
```

## API key
1. Get Your [Openai API keys](https://platform.openai.com/account/api-keys)
2. Add a text file named `apikey` in `src`
    ```
    xxxxxxxxx[YOUR_API_KEY]
    ```

**Important Action: Ensure the safety of your API keys. Never make them publicly accessible or upload them to a public repository.**

## Usage
Available programs
|Filename|Fucntion|
|--|--|
|src/text_chat.py| Text conversation|


Enter/Paste your content. Press Ctrl-D on a new line to submit.
```
User:
This is the first example.
This is a multiple lines example.
[Ctrl^D]
```
Press Ctrl-C to quit and save.
Logs with an empty title will be save as `last_chat.json`
```
User:
[Ctrl-C]
Enter a title for the chat: log_test
Chat log saved to file: [YOUR_PATH]/GPTtoolbox/saves/log_test_20230315_172229.json
```
Reload log by `-f`, print it by `-p`
```
$ python src/text_chat.py -f saves/last_chat.json -p
User:
test
AI:
This is a test response from an AI language model called GPT-3. It is designed to generate coherent and grammatically correct sentences to mimic human speech. As an AI language model, I do not have emotions or intentions. My primary goal is to provide informative and helpful responses to the user's requests. Please let me know if you need any assistance with a particular task!


Welcome to the GPT API! 
Enter/Paste your content. Press Ctrl-D on a new line to submit.
Press Ctrl-C to quit
User:
```