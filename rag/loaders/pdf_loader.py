from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

def load_pdf(path: str):
    loader = PyPDFLoader(path)
    docs = loader.load()
    for d in docs:
        d.metadata.setdefault("source", path)
        d.metadata["type"] = "pdf"
    return docs
