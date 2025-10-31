from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import logging
import os
import sys
import json
    
try:
    from ..agent import get_agent
except ImportError:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from agent import get_agent

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))
output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "output")

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
async def agent_config(request: Request):
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


@app.get("/output-files")
async def get_output_files():
    """Read all files from the output directory"""
    try:
        logger.info(output_dir)
        # Check if directory exists
        if not os.path.exists(output_dir):
            raise HTTPException(status_code=404, detail="Output directory not found")
        
        # Get list of all files
        files = []
        for filename in os.listdir(output_dir):
            filepath = os.path.join(output_dir, filename)
            
            # Only include files, not directories
            if os.path.isfile(filepath):
                file_size = os.path.getsize(filepath)
                files.append({
                    "name": filename,
                    "size": file_size,
                    "path": filepath
                })
        
        logger.info(f"Retrieved {len(files)} files from output directory")
        
        return {
            "status": "success",
            "directory": output_dir,
            "file_count": len(files),
            "files": files
        }
    
    except Exception as e:
        logger.error(f"Error reading output directory: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/output-files/{filename}")
async def read_output_file(filename: str):
    """Read specific file content from output directory and extract content field"""
    try:
        filepath = os.path.join(output_dir, filename)
        
        # Security check: prevent directory traversal attacks
        if not os.path.abspath(filepath).startswith(os.path.abspath(output_dir)):
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Check if file exists
        if not os.path.exists(filepath) or not os.path.isfile(filepath):
            raise HTTPException(status_code=404, detail="File not found")
        
        # Read file content
        with open(filepath, 'r', encoding='utf-8') as f:
            file_content = f.read()
        
        # Try to parse as JSON and extract content field
        try:
            json_data = json.loads(file_content)
            if isinstance(json_data, dict) and "content" in json_data:
                content = json_data["content"]
            else:
                content = file_content
        except json.JSONDecodeError:
            # Not JSON, return as is
            content = file_content
        
        logger.info(f"Read file: {filename}")
        
        return {
            "content": content
        }
    
    except UnicodeDecodeError:
        logger.error(f"Could not decode file as text: {filename}")
        raise HTTPException(status_code=400, detail="File is not readable as text")
    except Exception as e:
        logger.error(f"Error reading file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)