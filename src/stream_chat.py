from constant import *
from chat_gui import ChatWindow
from text_chat import TextLog

import tiktoken
import openai
import argparse

def main(args):
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

    try:
        encoding = tiktoken.encoding_for_model(chat_params['model'])
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    
    app = QApplication()

    chat_log = TextLog(args.file)
    client = StreamClient(chat_log, chat_params, encoding)
    chat_thread = StreamThread(client)
    chat_window = ChatWindow(client, chat_thread)

    # start the chat thread
    chat_thread.start()
    # show the chat window
    chat_window.show()
    # run the application event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--file", help="load a log file", type=str, default="")
    parser.add_argument("-p","--print", help="print loaded log file", action="store_true")
    args = parser.parse_args()
    main(args)