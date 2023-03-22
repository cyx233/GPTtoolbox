from utils import increase_usage
from .text_chat import text_chat
from PySide2.QtCore import QThread, Signal 

import os
import sys
import json
import threading

class StreamThread(QThread):
    message_received = Signal(str)

    def __init__(self, client):
        super().__init__()
        self.client = client
    
    def handle_response(self, response):
        collected_messages = []
        self.message_received.emit("AI:\n")
        for chunk in response:
            chunk_message = chunk["choices"][0]["delta"].get("content", "")  # extract the message
            if chunk_message == "\n\n":
                continue
            self.message_received.emit(chunk_message)
            collected_messages.append(chunk_message)
        self.message_received.emit("\n\n")
        return "".join(collected_messages)

    def run(self):
        while True:
            response = self.client.recv()
            sentence = self.handle_response(response)
            self.client.response_record(sentence)

class StreamClient:
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
    
    def send(self, message):
        if self._response:
            return False
        with self._lock:
            self._num_prompt, self._response = text_chat(message, self.chat_log, self.chat_params, self.encoding)
            if self._num_prompt==0:
                self._response = None
                return False
            self._cv.notify()
            return True

    def recv(self):
        with self._lock:
            self._cv.wait_for(lambda: self._response is not None)
            return self._response