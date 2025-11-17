from langchain_community.vectorstores import Chroma
from rag.embeddings import embeddings
import os

PERSIST_DIR = "./chroma_db"

def load_vectorstore():
    if os.path.exists(PERSIST_DIR):
      return Chroma(
      persist_directory=PERSIST_DIR,
      embedding_function=embeddings
      )    
    return None

def save_vectorstore(db):
    db.persist()