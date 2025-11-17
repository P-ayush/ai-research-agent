from rag.vector_store import load_vectorstore

def rag_tool_fn(query: str) -> str:
    db = load_vectorstore()
    if db is None:
        return "No vector index available. Please ingest documents first."

    retriever = db.as_retriever(search_kwargs={"k": 4})
    try:
        docs = retriever.get_relevant_documents(query)
    except Exception:
        docs = retriever.invoke(query)

    lines = []
    for i, d in enumerate(docs, start=1):
        src = d.metadata.get("source", "unknown")
        snippet = d.page_content[:600].replace("\n", " ").strip()
        lines.append(f"[{i}] Source: {src}\n{snippet}\n")
    return "\n".join(lines)
