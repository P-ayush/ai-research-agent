from rag.splitter import split_docs
from rag.vector_store import load_vectorstore, save_vectorstore
from rag.embeddings import embeddings
from rag.loaders.pdf_loader import load_pdf
from rag.loaders.csv_loader import load_csv
from rag.loaders.docx_loader import load_docx
from rag.loaders.url_loader import load_url
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from rag.llm import chat

def load_any(path):
   if path.startswith("http"):
    return load_url(path)
   if path.endswith(".pdf"):
    return load_pdf(path)
   if path.endswith(".csv"):
    return load_csv(path)
   if path.endswith(".docx"):
    return load_docx(path)
   raise Exception("Unsupported file type")

def ingest(path):
 docs = load_any(path)
 chunks = split_docs(docs)

 db = load_vectorstore()

 if db:
  db.add_documents(chunks)
 else:
  db = Chroma.from_documents(
  chunks,
  embeddings,
  persist_directory="./chroma_db"
  )
  save_vectorstore(db)
  return len(chunks)

prompt = ChatPromptTemplate.from_messages([
("system", "Answer based ONLY on the given context. If unsure, say 'I don't know'."),
("human", "Context:\n{context}\n\nQuestion: {question}\n\nAnswer:")
])

def rag_query(question: str):
  db = load_vectorstore()
  retriever = db.as_retriever(search_kwargs={"k": 4})


  docs = retriever.invoke(question)
  context = "\n\n".join([d.page_content for d in docs])


  messages = prompt.invoke({"context": context, "question": question})
  response = chat.invoke(messages)
  return response.content