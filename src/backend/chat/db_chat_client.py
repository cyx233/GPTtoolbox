from utils import increase_usage
from .db_text_chat import db_text_chat
from PySide2.QtCore import QThread, Signal 

import os
import sys
import json
import threading

class DatabaseChatClient:
    def __init__(self, chat_log, chat_params, encoding):
        self._lock = threading.Lock()
        self._cv = threading.Condition(self._lock)
        self._response = None
        self._num_prompt=0

        self.chat_log = chat_log
        self.chat_params = chat_params
        self.encoding = encoding

    def response_record(self, sentence):
        with self._lock:
            self.chat_log.append("assistant", sentence)

            increase_usage(
                self.chat_params['model'], 
                self._num_prompt+len(self.encoding.encode(sentence))
                )
            self._response = None
            self._num_prompt = 0
    
    def send(self, message, filenames):
        if self._response:
            return False
        with self._lock:
            self._num_prompt, self._response = db_text_chat(message, filenames, self.chat_log, self.chat_params, self.encoding)
            if self._num_prompt==0:
                self._response = None
                return False
            self._cv.notify()
            return True

    def recv(self):
        with self._lock:
            self._cv.wait_for(lambda: self._response is not None)
            return self._response