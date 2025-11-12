# build_faiss_index.py

from modules.embeddings_store import add_documents_to_faiss

# Sample text chunks for testing
chunks = [
    "The sun is the star at the center of the Solar System.",
    "Python is a versatile programming language.",
    "Water boils at 100 degrees Celsius."
]

source_file = "manual_test.txt"

add_documents_to_faiss(chunks, source_file)

print("✅ FAISS index created successfully.")
