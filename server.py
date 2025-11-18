from fastapi import FastAPI
from pydantic import BaseModel
from agent.agent import run_research

app = FastAPI(title="AI Research Agent API")

class ResearchRequest(BaseModel):
    query: str

@app.post("/research")
async def research_endpoint(req: ResearchRequest):
    try:
        result = run_research(req.query)
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
