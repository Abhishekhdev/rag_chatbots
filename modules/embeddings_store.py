from pathlib import Path
from typing import List, Optional

# ✅ Use HuggingFace embeddings for local & free document vectors
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings   # <-- UPDATED IMPORT

from modules.config import FAISS_DIR, INDEX_NAME

# Initialize local HuggingFace embeddings (no API key needed)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def create_or_load_faiss() -> Optional[FAISS]:
    """
    Loads existing FAISS index if available, otherwise returns None.
    """
    index_path = Path(FAISS_DIR) / f"{INDEX_NAME}.faiss"
    if index_path.exists():
        print("[INFO] Loading existing FAISS index...")
        return FAISS.load_local(
            str(FAISS_DIR),
            embeddings,
            index_name=INDEX_NAME,
            allow_dangerous_deserialization=True
        )
    else:
        print("[INFO] No FAISS index found. A new one will be created when documents are added.")
        return None

def add_documents_to_faiss(chunks: List[str], source_file: str) -> FAISS:
    """
    Add text chunks to FAISS index or create one if it doesn't exist.

    Args:
        chunks (List[str]): Text chunks to embed.
        source_file (str): Metadata info (typically the source filename).

    Returns:
        FAISS: The FAISS vector store with the added documents.
    """
    docs = [Document(page_content=c, metadata={"source": source_file}) for c in chunks]
    db = create_or_load_faiss()

    if db:
        db.add_documents(docs)
        print(f"[INFO] Added {len(chunks)} documents to existing FAISS index.")
    else:
        db = FAISS.from_documents(docs, embeddings)
        print(f"[INFO] Created new FAISS index with {len(chunks)} documents.")

    # Ensure directory exists before saving
    Path(FAISS_DIR).mkdir(parents=True, exist_ok=True)

    # Save updated index
    db.save_local(str(FAISS_DIR), index_name=INDEX_NAME)
    print(f"[INFO] FAISS index saved to '{FAISS_DIR}'.")

    return db
