import pdfplumber
import lmdb
import numpy as np
import openai
from PySide2.QtWidgets import QApplication, QFileDialog, QMessageBox, QProgressBar, QWidget, QVBoxLayout
from PySide2.QtCore import QSettings
import os
from utils import get_config, env, increase_usage

# Initialize OpenAI API key
openai.api_key = get_config('settings', 'api_key')

# Initialize LMDB database
db_path = get_config('settings', 'db_dir')

# Create two databases: one for storing text and one for storing embeddings
file_db = env.open_db(b'file_database')
chunk_db = env.open_db(b'chunk_database')
embedding_db = env.open_db(b'embedding_database')

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
    chunk_size = int(get_config('db_settings', 'chunk_size'))
    chunks = []
    for i in range(0, len(text), chunk_size):
        data = text[i:i+chunk_size]
        if data:
            chunks.append(data)
    return chunks

def get_embeddings_from_chunks(chunks, progress_callback):
    """
    Get embeddings for the given text chunks using OpenAI API.
    Returns a list of numpy arrays.
    """
    embeddings = []
    model = get_config('model', 'embedding')
    import time
    for i, chunk in enumerate(chunks):
        response = openai.Embedding.create(model=model, input=chunk)
        embedding = np.array(response['data'][0]["embedding"])
        embeddings.append(embedding)
        increase_usage(model, response['usage']['prompt_tokens'])
        progress_callback(i / len(chunks))
        QApplication.processEvents()
    return embeddings

def store_chunks_in_database(file_name, text_chunks, embedding_chunks):
    """
    Store the given text chunks and embedding chunks for the given file name in LMDB database.
    """
    # Store the file name in filename_db
    with env.begin(write=True) as txn:
        # Store the text chunks for the file
        text_key = f"{file_name}".encode()
        txn.put(text_key, str(len(text_chunks)).encode(), db=file_db)
        for i, text_chunk in enumerate(text_chunks):
            txn.put(f"{file_name}:{i}".encode(), text_chunk.encode(), db=chunk_db)
        # Store the embedding matrix for the file
        embedding_key = f"{file_name}:embeddings".encode()
        embeddings = np.vstack(embedding_chunks)
        txn.put(embedding_key, embeddings.tobytes(), db=embedding_db)

def process_file(file_path):
    """
    Read the PDF file, extract text, split into chunks, get embeddings, and store in database.
    """
    # Create a progress bar widget
    progress_bar = QProgressBar()
    # Set the progress bar to have a range from 0 to 100
    progress_bar.setRange(0, 100)
    # Connect the progress bar to the `valueChanged` signal of its QProgressBar
    progress_bar.valueChanged.connect(lambda value: progress_bar.setFormat(f"{value}%"))

    progress_widget = QWidget()
    progress_widget.setWindowTitle("Processing...")
    progress_widget_layout = QVBoxLayout()
    progress_widget_layout.addWidget(progress_bar)
    progress_widget.setLayout(progress_widget_layout)
    progress_widget.show()

    def progress_callback(progress):
        progress_bar.setValue(int(progress * 100))


    file_extension = os.path.splitext(file_path)[1]
    if file_extension == '.pdf':
        text = extract_text_from_pdf(file_path)
    else:
        with open(file_path) as f:
            text = f.read()
    text_chunks = split_text_to_chunks(text)
    if not text_chunks:
        return
    embedding_chunks = get_embeddings_from_chunks(text_chunks, progress_callback)
    store_chunks_in_database(os.path.basename(file_path), text_chunks, embedding_chunks)