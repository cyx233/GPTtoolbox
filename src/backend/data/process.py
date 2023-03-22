import pdfplumber
import lmdb
import numpy as np
import openai
from PySide2.QtWidgets import QApplication, QFileDialog, QMessageBox
from PySide2.QtCore import QSettings
import os
from utils import get_config, env

# Initialize OpenAI API key
openai.api_key = get_config('settings', 'api_key')

# Initialize LMDB database
db_path = get_config('settings', 'db_dir')

# Create two databases: one for storing text and one for storing embeddings
with env.begin(write=True) as txn:
    text_db = txn.open_db(b'text_database')
    embedding_db = txn.open_db(b'embedding_database')

# Define the chunk size for splitting the text
chunk_size = 2048

def extract_text_from_pdf(file_path):
    """
    Extract text from a PDF file and return as a string.
    """
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def split_text_to_chunks(text):
    """
    Split the given text into chunks with proper chunk size for OpenAI embedding API.
    Returns a list of text chunks.
    """
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i+chunk_size])
    return chunks

def get_embeddings_from_chunks(chunks):
    """
    Get embeddings for the given text chunks using OpenAI API.
    Returns a list of numpy arrays.
    """
    embeddings = []
    for chunk in chunks:
        response = openai.Embedding.create(engine="ada", input=chunk)
        embedding = np.array(response["embedding"])
        embeddings.append(embedding)
    return embeddings

def store_chunks_in_database(file_name, text_chunks, embedding_chunks):
    """
    Store the given text chunks and embedding chunks for the given file name in LMDB database.
    """
    # Store the file name in filename_db
    with env.begin(write=True) as txn:
        # Store the text chunks for the file
        text_key = f"{file_name}".encode()
        txn.put(text_key, str(len(text_chunks)).encode(), db=text_db)
        for i, text_chunk in enumerate(text_chunks):
            txn.put(f"{file_name}:{i}".encode(), text_chunk.encode(), db=text_db)

        # Store the embedding matrix for the file
        embedding_key = f"{file_name}:embeddings".encode()
        embeddings = np.vstack(embedding_chunks)
        txn.put(embedding_key, embeddings.tobytes(), db=embedding_db)

def process_file(file_path):
    """
    Read the PDF file, extract text, split into chunks, get embeddings, and store in database.
    """
    text = extract_text_from_pdf(file_path)
    text_chunks = split_text_to_chunks(text)
    embedding_chunks = get_embeddings_from_chunks(text_chunks)
    store_chunks_in_database(os.path.basename(fila_path), text_chunks, embedding_chunks)