from langchain_core.prompts import ChatPromptTemplate
from rag.llm import chat

report_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert research analyst. "
        "You synthesize information from RAG context, web searches, and summaries. "
        "Your output must be factual, structured, clean, and extremely well-formatted in Markdown. "
        "Avoid raw backslashes, escape characters, or sloppy formatting."
    ),
    (
        "human",
        """
Prepare a final research report using this information:

### Topic
{query}

### RAG Findings
{rag}

### Web Findings
{web}

### Summaries / Extracted Insights
{summary}

---

## FORMAT REQUIREMENTS  
You MUST follow this structure exactly:

# Research Report: {query}

## Executive Summary
- 3–5 sentences
- High-level overview
- No bullet points here

## Key Findings
- 5–10 bullet points
- Each bullet max 1–2 sentences
- Must be factual and concise

## Detailed Insights
Write 3–6 paragraphs.  
Each paragraph:
- Begins with a bold subheading  
- Contains well-structured analysis  
- Integrates RAG + web + summary findings  

## Table Summary (if applicable)
Provide a clean Markdown table:
| Category | Insight | Source |
|---------|----------|--------|
| ...     | ...      | ...    |

## Sources
List ALL unique sources extracted from RAG + web results.  
Format:
- Source Name — URL (if available)

Ensure:
- No stray '\\n' sequences  
- No repeated content  
- No hallucinations  
- No merged markdown syntax  
- Clean whitespace  
        """
    )
])

def generate_report(query: str, rag: str, web: str, summary: str) -> str:
    """Generate a professional, cleanly formatted research report."""
    messages = report_prompt.invoke({
        "query": query,
        "rag": rag,
        "web": web,
        "summary": summary
    })

    response = chat.invoke(messages)
    return response
