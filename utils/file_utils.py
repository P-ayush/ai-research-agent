import os
from rag.loaders.pdf_loader import load_pdf
from rag.loaders.csv_loader import load_csv
from rag.loaders.docx_loader import load_docx
from rag.loaders.url_loader import load_url

def load_any(path: str):
    path = path.strip()

    if path.startswith("http://") or path.startswith("https://"):
        return load_url(path)

    ext = os.path.splitext(path)[1].lower()

    if ext == ".pdf":
        return load_pdf(path)

    elif ext == ".csv":
        return load_csv(path)

    elif ext == ".tsv":
        return load_csv(path)

    elif ext == ".docx":
        return load_docx(path)

    else:
        raise ValueError(f"Unsupported file type: {ext}")
