import pandas as pd
from langchain_core.documents import Document

def load_csv(path: str):
    df = pd.read_csv(path)
    content = df.to_string()
    return [Document(page_content=content, metadata={"source": path, "type": "csv"})]
