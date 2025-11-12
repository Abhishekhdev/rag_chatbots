# ingest.py

import argparse
from pathlib import Path
from modules.text_extraction import extract_text
from modules.text_processing import chunk_text
from modules.embeddings_store import add_documents_to_faiss
from modules.config import UPLOAD_DIR

# Ensure upload directory exists
Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

def ingest_file(file_path):
    print(f"Ingesting file: {file_path}")
    text = extract_text(file_path)
    chunks = chunk_text(text)
    add_documents_to_faiss(chunks, Path(file_path).name)
    print("Document ingested successfully!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest a document into RAG chatbot")
    parser.add_argument("file", type=str, help="Path to the file to ingest")
    args = parser.parse_args()

    ingest_file(args.file)
