from utils import api_key
from gui import ChatWindow
from backend.chat import TextLog, StreamClient, StreamThread

from PySide2.QtWidgets import QApplication
import sys
import tiktoken
import openai
import argparse

def stream_chat(model="gpt-3.5-turbo", load_log="", user=""):
    # Set your API key
    openai.api_key = api_key.strip()

    # Set the chatbot's parameters
    chat_params = {
        "model": model,
        "n":1,
        "stream":True,
        "user":user
    }

    try:
        encoding = tiktoken.encoding_for_model(chat_params['model'])
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    
    app = QApplication()

    chat_log = TextLog(load_log)
    client = StreamClient(chat_log, chat_params, encoding)
    chat_thread = StreamThread(client)
    chat_window = ChatWindow(client, chat_thread)

    # start the chat thread
    chat_thread.start()
    # show the chat window
    chat_window.show()
    # run the application event loop
    sys.exit(app.exec_())