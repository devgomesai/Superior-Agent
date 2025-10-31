# Superior-Agent 🤖⛏️

AI-powered stock analysis agent with multi-agent system for comprehensive market research and financial analysis.

![Architecture Diagram](./architecture.png)

[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/langgraph-1.0.1-4D97FF)](https://github.com/langchain-ai/langgraph)
[![FastAPI](https://img.shields.io/badge/fastapi-0.115.0+-009688)](https://fastapi.tiangolo.com/)

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [Development](#development)

## Features

- **Multi-Agent Architecture**: Three specialized agents work together to provide comprehensive stock analysis
- **Real-time Market Data**: Fetches live stock prices, performance metrics, and financial data
- **Market Intelligence**: Uses Perplexity API to gather the latest news, trends, and analyst opinions
- **Automated Reports**: Generates professional markdown reports from the analysis
- **Web API**: FastAPI interface for easy integration and access
- **Interactive Web Interface**: User-friendly dashboard for stock analysis
- **Workflow Visualization**: Mermaid graph visualization of the agent workflow
- **Customizable Prompts**: Configurable system prompts for different analysis needs

## Architecture

### Overview

The Superior-Agent system consists of three specialized agents coordinated by a supervisor using LangGraph's multi-agent orchestration:

- **Web Search Expert**: Gathers current market news, trends, and analyst opinions using Perplexity API
- **Finance Analyst**: Fetches stock prices, performance metrics, and financial data using yfinance
- **Report Generator**: Compiles all gathered data into professional markdown reports
- **Supervisor**: Orchestrates the workflow between agents to generate comprehensive analyses

### Workflow

1. **Financial Manager Agent** (supervisor) receives the analysis query and coordinates the workflow
2. **Web Search Agent** uses Perplexity API to gather market news and trends
3. **Yahoo Finance Agent** fetches live stock prices, performance metrics, and financial data
4. **Report Generator Agent** compiles all gathered information into a professional report
5. **Reports** are saved as markdown files in the `output/` directory

## Tech Stack

- [LangGraph](https://github.com/langchain-ai/langgraph) - State management and multi-agent orchestration
- [LangGraph Supervisor](https://pypi.org/project/langgraph-supervisor/) - Multi-agent supervisor functionality
- [LangChain](https://github.com/langchain-ai/langchain) - LLM integration and tool management
- [FastAPI](https://fastapi.tiangolo.com/) - Web API framework
- [yfinance](https://github.com/ranaroussi/yfinance) - Financial data fetching
- [Perplexity API](https://www.perplexity.ai/) - Market research and news gathering
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation
- [uvicorn](https://www.uvicorn.org/) - ASGI server
- [Jinja2](https://jinja.palletsprojects.com/) - Template rendering
- [IPython](https://ipython.org/) - Interactive Python functionality
- [Streamlit](https://streamlit.io/) - Optional web application framework

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/devgomesai/Superior-Agent.git
   cd superior-agent
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   # Using pip
   pip install -e .
   
   # Or using uv (recommended)
   uv pip install -e .
   ```

## Configuration

1. Create a `.env` file in the project root directory:

   ```env
   # Perplexity API key for market research
   PERPLEXITY_API_KEY=your_perplexity_api_key_here

   # LLM provider and model selection
   # Examples: groq:mixtral-8x7b-32768, anthropic:claude-3-5-sonnet-20241022
   LLM_CHOICE=groq:mixtral-8x7b-32768

   # API keys for your selected LLM provider
   GROQ_API_KEY=gsk_your_groq_api_key_here
   ANTHROPIC_API_KEY=sk-ant-your_anthropic_api_key_here
   ```

   For more LLM options, refer to the [LangChain documentation](https://python.langchain.com/api_reference/langchain/chat_models/langchain.chat_models.base.init_chat_model.html).

2. The application automatically uses these environment variables for:
   - Perplexity API authentication for market research
   - LLM model selection and credentials

## Usage

### API Mode (Recommended)

1. Start the API server:
   ```bash
   uvicorn src.agent.api.api:app --reload
   ```

   Or without auto-reload:
   ```bash
   uvicorn src.agent.api.api:app
   ```

2. Access the application:
   - Web interface: `http://127.0.0.1:8000`
   - API documentation: `http://127.0.0.1:8000/docs`

### API Endpoints

- **POST `/analyze`** - Analyze stock using the agent workflow
  ```bash
  curl -X POST "http://127.0.0.1:8000/analyze" \
    -H "Content-Type: application/json" \
    -d '{"query": "Analyze Tesla stock (TSLA) performance and financial metrics"}'
  ```

- **GET `/`** - Home page with stock analysis interface

- **GET `/health`** - Health check endpoint
  ```bash
  curl -X GET "http://127.0.0.1:8000/health"
  ```

- **GET `/output-files`** - List all generated stock reports
  ```bash
  curl -X GET "http://127.0.0.1:8000/output-files"
  ```

- **GET `/output-files/{filename}`** - Get specific report content
  ```bash
  curl -X GET "http://127.0.0.1:8000/output-files/stock_report_AAPL_20251027_094248.md"
  ```

### Interactive Command-Line Mode

Run the application directly for interactive analysis:

```bash
python -m src.tests.main
```

Or from the src directory:

```bash
cd src
python -m tests.main
```

Follow the prompts to enter your stock analysis query.

### Web Interface Features

The interactive web interface (`http://127.0.0.1:8000`) includes:

- Stock query input form for analysis requests
- Real-time display of agent workflow and responses
- Download section for previously generated reports
- Refresh functionality to update report listings
- Syntax-highlighted JSON response viewer

## Project Structure

```
superior-agent/
├── src/
│   ├── agent/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── api.py                    # FastAPI endpoints
│   │   ├── __init__.py
│   │   └── agent.py                      # Core agent workflow
│   ├── prompts/
│   │   └── agent_prompts.py              # Agent system prompts
│   ├── templates/
│   │   └── index.html                    # Web interface
│   ├── tests/
│   │   ├── main.py                       # Interactive CLI mode
│   │   ├── test.py                       # Test template
│   │   └── tests.py                      # Test utilities
│   ├── tools/
│   │   └── stock_analysis_tools.py       # Market data tools
│   ├── __init__.py
│   └── requirements.txt
├── output/                               # Generated stock reports
├── .gitignore
├── .python-version
├── agent_flow.json                       # Workflow configuration
├── architecture.png                      # Architecture diagram
├── Dockerfile
├── graph.png                             # Workflow visualization
├── pyproject.toml                        # Project configuration
├── README.md
├── trace.png                             # Debug trace
└── uv.lock
```

## Customization

### Prompts

Customize agent behavior in `src/prompts/agent_prompts.py`:

- `WEB_SEARCH_AGENT_PROMPT` - Web research agent configuration
- `YAHOO_FINANCE_AGENT_PROMPT` - Finance analyst configuration
- `REPORT_GENERATOR_AGENT_PROMPT` - Report generator configuration
- `SUPERVISOR_PROMPT` - Workflow coordinator configuration

### Tools

Available tools in `src/tools/stock_analysis_tools.py`:

- `web_search_news()` - Search market news using Perplexity API
- `get_stock_price()` - Fetch current stock price and information
- `get_stock_performance()` - Retrieve historical performance data
- `get_financial_metrics()` - Get key financial metrics
- `save_report_to_file()` - Save analysis reports to markdown

### Configuration Files

- `pyproject.toml` - Project metadata and dependencies
- `agent_flow.json` - Agent workflow configuration
- `graph.png` - Auto-generated workflow visualization

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **API Keys Invalid** | Verify your Perplexity and LLM API keys have sufficient credits |
| **No Internet Connection** | The system requires internet for fetching financial data and research |
| **LLM Access Error** | Ensure your LLM API key is properly configured in `.env` |
| **Rate Limits Exceeded** | Be aware of API rate limits for Perplexity and Yahoo Finance |
| **Port 8000 Already in Use** | Specify a different port: `uvicorn src.agent.api.api:app --port 8001` |

## Development

### Setup

Install the package in editable mode for development:

```bash
pip install -e .
```

### Running Tests

Test scripts are located in `src/tests/`:

- `main.py` - Interactive command-line interface for testing
- `test.py` - Test template (commented)
- `tests.py` - Additional test utilities

Run interactive analysis to test functionality:

```bash
python -m src.tests.main
```

### Workflow Visualization

The application automatically generates workflow visualizations (`graph.png`) when run, useful for debugging the agent flow.

## Acknowledgments

- [LangChain](https://github.com/langchain-ai/langchain) and [LangGraph](https://github.com/langchain-ai/langgraph) for the multi-agent framework
- [yfinance](https://github.com/ranaroussi/yfinance) for financial data access
- [Perplexity](https://www.perplexity.ai/) for market research capabilities
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [Jinja2](https://jinja.palletsprojects.com/) for template rendering