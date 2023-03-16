from constant import *
import openai

def get_user_input() :
    print("User:")
    contents = []
    while True:
        try:
            line = input().strip()
        except EOFError:
            break
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        contents.append(line)
    return "\n".join(contents)

# Define the function to send a message to the chatbot and get a response
def chat(message, chat_log, chat_params, prompt_func=None):
    if prompt_func:
        message = prompt_func(message)
    chat_log.append({"role":"user", "content":message})
    response = openai.ChatCompletion.create(
        messages=chat_log,
        **chat_params
    )
    print("AI:")
    collected_messages = []
    for chunk in response:
        # skip header 
        # header \n\n content
        chunk_message = chunk["choices"][0]["delta"].get("content", "")  # extract the message
        if chunk_message == "\n\n":
            continue
        print(chunk_message,end="",flush=True)
        collected_messages.append(chunk_message)
    chat_log.append({"role": "assistant", "content":"".join(collected_messages)})
    print("\n")
    return chat_log