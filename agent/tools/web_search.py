from ddgs import DDGS

def web_search_tool(query: str, limit: int = 5):
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=limit)
        return results

