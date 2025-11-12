# modules/text_processing.py

from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_text(text, chunk_size=1000, chunk_overlap=200):
    """
    Split text into chunks for embeddings.
    chunk_size: number of characters per chunk
    chunk_overlap: number of overlapping characters
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = splitter.split_text(text)
    return chunks
