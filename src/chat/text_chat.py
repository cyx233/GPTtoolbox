import tiktoken
from constant import *
import openai

class TextLog:
    def __init__(self, filename=""):
        self._data = []
        self._begin = 0
        if filename:
            self.load(filename)

    def __str__(self):
        return self._str(self._begin)

    def __len__(self):
        return len(self._data) - self._begin

    def _str(self, begin):
        formatted = map(lambda m: "User:\n" + m['content'] + "\n" if m['role'] == "user" 
                             else "AI:\n" + m['content'] + "\n" if m['role'] == "assistant" 
                             else "", 
                        self._data[begin:])
        return ''.join(formatted) + '\n'

    def get_logs(self):
        return self._data[self._begin:]

    def pop(self):
        return self._data.pop()

    def all_str(self):
        return self._str(0)

    def append(self, role, message):
        self._data.append({"role":role, "content":message})

    def num_tokens_from_messages(self, encoding):
        """Returns the number of tokens used by a list of messages."""
        num_tokens = 0
        for message in self._data[self._begin:]:
            num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens

    def popleft(self):
        self._begin+=1
        return self._data[self._begin-1]
    
    def pop(self):
        self._begin = 0
        return self._data[-1]
    
    def save(self,filename):
        with open(filename, 'w') as f:
            json.dump(self._data, f)

    def load(self, filename):
        with open(filename) as f:
            self._data = json.load(f)


# Define the function to send a message to the chatbot and get a response
def text_chat(message, chat_log:TextLog, chat_params, encoding, prompt_func=None, prompt_limit=2048):
    if prompt_func:
        message = prompt_func(message)
    chat_log.append("user", message)

    num_prompt = chat_log.num_tokens_from_messages(encoding)
    # limit of input length
    while num_prompt >= prompt_limit:
        chat_log.popleft()
        num_prompt = chat_log.num_tokens_from_messages(encoding)

    if len(chat_log) == 0:
        chat_log.pop()
        return 0, [], None

    response = openai.ChatCompletion.create(
        messages=chat_log.get_logs(),
        **chat_params
    )

    return num_prompt, response