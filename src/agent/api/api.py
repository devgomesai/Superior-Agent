from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod, NodeStyles
import logging
    
try:
    from ..agent import get_agent
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from agent import get_agent
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

os.makedirs("output", exist_ok=True)

# Initialize agent app
agent_app = get_agent()

try:
    agent_app.get_graph().draw_mermaid_png(
        curve_style=CurveStyle.LINEAR,
        node_colors=NodeStyles(
            first="#FF6B6B",  # Vibrant red for start
            last="#4ECDC4",  # Teal for end
            default="#95E1D3",  # Mint green for regular nodes
        ),
        wrap_label_n_words=9,
        output_file_path='graph.png',
        background_color="white",
        padding=20,
    )
except Exception as e:
    print(f"Could not generate graph image: {e}")


@app.get("/")
async def agent_config():
    """Home endpoint with stock agent information"""
    return {
        "name": "Stock Analysis Agent",
        "description": "AI-powered stock analysis and research agent",
        "version": "1.0.1",
        "endpoints": {
            "health": "/health",
            "analyze": "/analyze"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/analyze")
async def analyze(request: AnalysisRequest):
    """Analyze stock using the agent workflow"""
    try:
        logger.info(f"Analyzing: {request.query}")
        
        result = agent_app.invoke({
            "messages": [{"role": "user", "content": request.query}]
        })
        
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