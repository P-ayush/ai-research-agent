from rag.llm import chat
from langchain_core.prompts import ChatPromptTemplate
from langchain.tools import tool

summary_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a factual summarizer. Extract 5 key facts and cite sources when provided."),
    ("human", "Context:\n{context}\n\nProduce a concise bullet list of key facts (max 8) and a 2-sentence summary.")
])


@tool
def summarize_fn(text: str) -> str:
    """Summarize long content."""
    if not text or text.strip() == "":
        return "No text provided to summarize."

    messages = summary_prompt.invoke({"context": text})

    response = chat.invoke(messages)

    return response.content
