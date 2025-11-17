from langchain_community.document_loaders import Docx2txtLoader

def load_docx(path: str):
    loader = Docx2txtLoader(path)
    docs = loader.load()
    for d in docs:
        d.metadata.setdefault("source", path)
        d.metadata["type"] = "docx"
    return docs
