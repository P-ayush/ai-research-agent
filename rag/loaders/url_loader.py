from langchain_community.document_loaders import WebBaseLoader

def load_url(url: str):
    loader = WebBaseLoader(url)
    docs = loader.load()
    for d in docs:
        d.metadata.setdefault("source", url)
        d.metadata["type"] = "url"
    return docs
