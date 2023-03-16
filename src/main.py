import os
import openai
import time
import json
import argparse

# Set your API key
with open("apikey") as f:
    openai.api_key = f.read().strip()

# Set the chatbot's parameters
chat_params = {
    "model": "gpt-3.5-turbo",
    "n":1,
    "stream":True,
    "user":"cyxisaac@gmail.com"
}


# Define the function to send a message to the chatbot and get a response
def chat(message, chat_log=None):
    if chat_log is None:
        chat_log = []
    chat_log.append({"role":"user", "content":message})
    try:
        response = openai.ChatCompletion.create(
            messages=chat_log,
            **chat_params
        )
    except Error as e:
        print(e)
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

def get_input():
    print("User:")
    contents = []
    while True:
        try:
            line = input().strip()
        except EOFError:
            break
        contents.append(line)
    return "\n".join(contents)

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
    conversation_title = ""
    save_dir = "../saves"
    os.makedirs(save_dir, exist_ok=True)
    print("Welcome to the GPT API! Type '@quit' to exit.")
    print("Enter/Paste your content. Press Ctrl-D on a new line to submit.")
    while True:
        message = get_input()
        if message.lower() == "@quit":
            # Prompt for conversation title and save conversation log to file
            while not conversation_title:
                conversation_title = input("Enter a title for the conversation: ")
            filename = os.path.join(save_dir,time.strftime(f"{conversation_title}_%Y%m%d_%H%M%S.json"))
            with open(filename, 'w') as f:
                json.dump(chat_log, f)
            print("Conversation log saved to file: " + filename)
            break
        chat_log = chat(message, chat_log)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--file", help="load a log file", type=str, default="")
    parser.add_argument("-p","--print", help="print loaded log file", action="store_true")
    args = parser.parse_args()
    main(args)