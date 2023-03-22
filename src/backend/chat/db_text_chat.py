import lmdb
import numpy as np
import openai
from utils import env, get_config
from .text_chat import TextLog

# Initialize OpenAI API key
openai.api_key = get_config('settings', 'api_key')

# Initialize LMDB database

# Open the databases for text and embeddings
file_db = env.open_db(b'file_database')
chunk_db = env.open_db(b'chunk_database')
embedding_db = env.open_db(b'embedding_database')

# Define the chunk size for splitting the text
chunk_size = get_config('db_settings', 'chunk_size')

def get_embeddings_for_filenames(filenames):
    """
    Get the embedding matrix for the given filenames from the LMDB database.
    """
    embeddings = []
    with env.begin(write=False) as txn:
        for filename in filenames:
            embedding_key = f"{filename}:embeddings".encode()
            embedding_bytes = txn.get(embedding_key, db=embedding_db)
            embedding = np.frombuffer(embedding_bytes, dtype=np.float32).reshape(-1, 1536)
            embeddings.append(embedding)
    return np.vstack(embeddings)

def get_text_chunk_for_index(filename, index):
    """
    Get the text chunk for the given filename and index from the LMDB database.
    """
    with env.begin(write=False) as txn:
        text_key = f"{filename}:{index}".encode()
        text = txn.get(text_key, db=chunk_db)
    return text.decode()

def add_chunks_to_prompt(prompt, embeddings, prompt_limit):
    """
    Add chunks to the prompt until the maximum token limit is reached.
    Returns the modified prompt and the number of tokens in the prompt.
    """
    num_tokens = len(openai.Completion.create(prompt=prompt)["choices"][0]["text"].split())
    i = 0
    while i < len(embeddings) and num_tokens < prompt_limit:
        chunk_text = get_text_chunk_for_index(filename, i)
        prompt += chunk_text
        num_tokens += len(chunk_text.split())
        i += 1
    return prompt, num_tokens

def build_prompt(message, filenames, prompt_limit):
    """
    Build a prompt for the given message and filenames.
    """
    embeddings = get_embeddings_for_filenames(filenames)
    # Calculate the similarity between the message embedding and the embeddings for the files
    similarity_scores = openai.VectorSimilarity.list(vector=message, vectors=list(embeddings))
    # Get the indices of the top 100 most similar embeddings
    top_indices = [score["vector_index"] for score in similarity_scores["data"][:100]]
    # Get the text chunks for the top 100 embeddings and add them to the prompt
    prompt = ""
    for index in top_indices:
        filename = filenames[index]
        chunk_text = get_text_chunk_for_index(filename, 0)
        prompt += chunk_text
        # If the prompt is still under the token limit, add more chunks
        if len(prompt.split()) < prompt_limit:
            prompt, _ = add_chunks_to_prompt(prompt, embeddings[index:], prompt_limit)
    return prompt

# Define the function to send a message to the chatbot and get a response
def db_text_chat(message, filenames, chat_log:TextLog, chat_params, encoding, prompt_limit=2048):
    
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