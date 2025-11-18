from langchain.tools import tool
from ddgs import DDGS

@tool
def web_search(query: str) -> str:
    """Search the live internet using DuckDuckGo and return summarized results."""

    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=5)

    lines = []
    for i, r in enumerate(results, start=1):
        title = r.get("title", "No title")
        href = r.get("href", "")
        body = r.get("body", "")[:300].replace("\n", " ")

        lines.append(f"[{i}] {title}\nURL: {href}\n{body}\n")

    return "\n".join(lines) if lines else "No web results found."
