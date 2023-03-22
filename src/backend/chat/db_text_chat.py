import lmdb
import numpy as np
import openai
from utils import env, get_config, increase_usage
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
    num_chunks = []
    with env.begin(write=False) as txn:
        for filename in filenames:
            embedding_key = f"{filename}:embeddings".encode()
            embedding_bytes = txn.get(embedding_key, db=embedding_db)
            embedding = np.frombuffer(embedding_bytes, dtype=np.float32).reshape(-1, 1536)
            embeddings.append(embedding)
            num_chunks.append(embedding.shape[0])
    return np.vstack(embeddings), num_chunks

def get_text_for_index(filename, index):
    """
    Get the text chunk for the given filename and index from the LMDB database.
    """
    with env.begin(write=False) as txn:
        text_key = f"{filename}:{index}".encode()
        text = txn.get(text_key, db=chunk_db)
    return text.decode()


def get_num_chunks(filename):
    with env.begin(write=False) as txn:
        num_key = f"{filename}".encode()
        num_chunks = txn.get(num_key, db=file_db)
    return int(num_chunks.decode())


# Define the function to send a message to the chatbot and get a response
def db_text_chat(message, filenames, chat_log:TextLog, chat_params, encoding, prompt_limit=2048):
    model = chat_params['model']
    response = openai.Embedding.create(model=model, input=message)
    query = np.array(response['data'][0]["embedding"])
    increase_usage(model, response['usage']['prompt_tokens'])

    keys = get_embeddings_for_filenames(filenames)

    similarities = np.dot(keys, query) / (np.linalg.norm(keys, axis=1) * np.linalg.norm(query))
    sorted_indices = np.argsort(similarities)[::-1]  # sort indices in descending order
    cur_file = 0
    begin = 0
    for i in sorted_indices:
        num_chunks = get_num_chunks(filenames[cur_file])
        while begin + num_chunks <= i:
            begin += num_chunks
            cur_file += 1
            num_chunks = get_num_chunks(filenames[cur_file])
        text = get_text_for_index(filename[cur_file], i - begin)
        chat_log.append('user', text)
        num_prompt = chat_log.num_tokens_from_messages(encoding)
        # limit of input length
        if num_prompt >= prompt_limit:
            chat_log.revert_append()
            num_prompt = chat_log.num_tokens_from_messages(encoding)
            break

    response = openai.ChatCompletion.create(
        messages=chat_log.get_logs(),
        **chat_params
    )

    return num_prompt, response