import json
from langchain.agents import create_react_agent, AgentExecutor,create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

from agent.memory import get_memory

from agent.tools.rag_tool import rag_tool_fn
from agent.tools.web_search import web_search
from agent.tools.summarizer import summarize_fn
from agent.tools.report_generator import generate_report

from rag.llm import chat


SYSTEM_PROMPT = """
You are an advanced AI Research Agent.

Your abilities:
1. Search internal documents (RAG)
2. Search the live internet (Web)
3. Summarize long content
4. Generate a final structured research report

Use tools when needed. Think step-by-step.
Always produce a final answer.
""".strip()


PROMPT = ChatPromptTemplate.from_messages([
    ("system",
    """
You are an advanced AI Research Agent.

Your job:
- Use tools when needed 
- Think step-by-step
- Always produce a final answer
    """
    ),
    ("human", "{input}"),
    ("ai", "{agent_scratchpad}")
])


def create_agent():
    tools = [
        rag_tool_fn,
        web_search,
        summarize_fn   
    ]

    agent = create_tool_calling_agent(
        llm=chat,
        tools=tools,
        prompt=PROMPT
    )

    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=get_memory(),
        verbose=True
    )

    return executor


def run_research(query: str):
    agent = create_agent()

    agent_response = agent.invoke({"input": query})
    def clean(text):
        if not isinstance(text, str):
            return text
        return text.replace("\\n", "\n").replace("\\", "").strip()

    agent_output = clean(agent_response.get("output", ""))

    rag = rag_tool_fn.invoke(query)
    web = web_search.invoke(query)
    summary = summarize_fn.invoke(rag + "\n\n" + web)

    payload = json.dumps({  
        "query": query,
        "rag": rag,
        "web": web,
        "summary": summary
    })

    report_raw = generate_report(query, rag, web, summary)

    if hasattr(report_raw, "content"):
        report = report_raw.content
    elif isinstance(report_raw, dict) and "content" in report_raw:
        report = report_raw["content"]
    else:
        report = str(report_raw)

    return {
        "agent_output": agent_output,
        "rag": rag,
        "web": web,
        "summary": summary,
        "report": report
    }


if __name__ == "__main__":
    q = input("Enter research topic: ")
    data = run_research(q)

    print("\n================= FINAL REPORT =================\n")
    print(data["report"])
