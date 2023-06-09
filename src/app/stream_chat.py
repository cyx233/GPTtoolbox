from utils import get_config
from gui import ChatWindow
from backend.chat import TextLog, StreamClient, StreamThread
from PySide2.QtCore import QEventLoop

import sys
import tiktoken
import openai
import argparse

def stream_chat(load_log="", user=""):
    # Set your API key
    openai.api_key = get_config('settings', 'api_key').strip()

    # Set the chatbot's parameters
    chat_params = {
        "model": get_config('model', 'llm'),
        "n":1,
        "stream":True,
        "user":user
    }

    try:
        encoding = tiktoken.encoding_for_model(chat_params['model'])
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    
    chat_log = TextLog(load_log)
    client = StreamClient(chat_log, chat_params, encoding)
    chat_thread = StreamThread(client)
    chat_window = ChatWindow(client, chat_thread)

    # start the chat thread
    chat_thread.start()
    # show the chat window
    chat_window.show()

    loop = QEventLoop()
    loop.exec_()