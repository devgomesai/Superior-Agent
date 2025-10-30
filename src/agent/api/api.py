from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import logging
    
try:
    from ..agent import get_agent
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from agent import get_agent

import os
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))

# Initialize FastAPI app
app = FastAPI(
    title="Stock Analysis Agent API",
    version="1.0.0"
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic model
class AnalysisRequest(BaseModel):
    query: str


# Initialize agent app
agent_app = get_agent()


@app.get("/", response_class=HTMLResponse)
async def agent_config( request: Request):
    """Home endpoint with stock agent information"""
    return templates.TemplateResponse(
        "index.html", {"request": request}
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/analyze")
async def analyze(request: AnalysisRequest):
    """Analyze stock using the agent workflow"""
    try:
        logger.info(f"Analyzing: {request.query}")
        
        result = agent_app.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": request.query
                }
            ]
        }
    )
        
        return {
            "status": "success",
            "result": result
        }
    
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)