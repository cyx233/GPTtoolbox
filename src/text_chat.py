import os
import openai
import time
import json
import argparse
from utils import *

# Set your API key
with open(keyfile) as f:
    openai.api_key = f.read().strip()

# Set the chatbot's parameters
chat_params = {
    "model": "gpt-3.5-turbo",
    "n":1,
    "stream":True,
    "user":"cyxisaac@gmail.com"
}

def main(args):
    # Start the chat
    chat_log = []
    if args.file:
        with open(args.file) as f:
            chat_log = json.load(f)
        if args.print:
            for m in chat_log:
                if m['role'] == "user":
                    print("User:\n" + m['content'])
                elif m['role']=="assistant":
                    print("AI:\n" + m['content'])
            print("\n")
    chat_title = ""
    os.makedirs(save_dir, exist_ok=True)
    print("Welcome to the GPT API!")
    print("Enter/Paste your content. Press Ctrl-D on a new line to submit.")
    print("Press Ctrl-C to quit")
    while True:
        try:
            message = get_user_input()
        except KeyboardInterrupt:
            # Prompt for chat title and save chat log to file
            print("")
            try:
                chat_title = input("Enter a title for the chat: ")
            except KeyboardInterrupt: 
                print("")
            if chat_title:
                filename = os.path.join(save_dir,time.strftime(f"{chat_title}_%Y%m%d_%H%M%S.json"))
            else:
                filename = os.path.join(save_dir,"last_chat.json")
            with open(filename, 'w') as f:
                json.dump(chat_log, f)
            print("Chat log saved to file: " + filename)
            break
        chat_log = chat(message, chat_log, chat_params)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--file", help="load a log file", type=str, default="")
    parser.add_argument("-p","--print", help="print loaded log file", action="store_true")
    args = parser.parse_args()
    main(args)