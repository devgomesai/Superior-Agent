# Superior-Agent 🤖⛏️

AI-powered stock analysis agent with multi-agent system for comprehensive market research and financial analysis.

[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/langgraph-1.0.1-4D97FF)](https://github.com/langchain-ai/langgraph)
[![FastAPI](https://img.shields.io/badge/fastapi-0.115.0+-009688)](https://fastapi.tiangolo.com/)

## 🚀 Features

- **Multi-Agent Architecture**: Three specialized agents work together to provide comprehensive stock analysis
- **Real-time Market Data**: Fetches live stock prices, performance metrics, and financial data
- **Market Intelligence**: Uses Perplexity API to gather the latest news, trends, and analyst opinions
- **Automated Reports**: Generates professional markdown reports from the analysis
- **Web API**: FastAPI interface for easy integration and access
- **Workflow Visualization**: Mermaid graph visualization of the agent workflow
- **Customizable Prompts**: Configurable system prompts for different analysis needs

## 🏗️ Architecture Overview

The Superior-Agent system consists of three specialized agents coordinated by a supervisor using LangGraph's multi-agent orchestration system. The project is organized into several core directories and modules that serve different purposes in the analysis pipeline:

### Project Structure

```
Superior-Agent/
├── output/                    # Generated stock analysis reports
├── src/                       # Source code
│   ├── agent/                 # Core agent logic and API interface
│   │   ├── api/               # FastAPI web interface
│   │   └── agent.py           # Main agent workflow implementation
│   ├── prompts/               # System prompts for each agent
│   ├── templates/             # HTML templates for web interface
│   ├── tests/                 # Test scripts and interactive mode
│   └── tools/                 # Stock analysis tools and utilities
├── agent_flow.json            # Agent workflow configuration
├── graph.png                  # Visual representation of the workflow
├── requirements.txt           # Python dependencies
├── pyproject.toml             # Project configuration
└── README.md                  # Documentation
```

The system consists of these specialized agents coordinated by a supervisor:

- **Web Search Expert**: Gathers current market news, trends, and analyst opinions using Perplexity API
- **Finance Analyst**: Fetches stock prices, performance metrics, and financial data using yfinance
- **Report Generator**: Compiles all gathered data into professional markdown reports
- **Supervisor**: Orchestrates the workflow between agents to generate comprehensive analyses

## 🛠️ Technology Stack

- [LangGraph](https://github.com/langchain-ai/langgraph) - State management and multi-agent orchestration
- [LangChain](https://github.com/langchain-ai/langchain) - LLM integration and tool management
- [FastAPI](https://fastapi.tiangolo.com/) - Web API framework
- [yfinance](https://github.com/ranaroussi/yfinance) - Financial data fetching
- [Perplexity API](https://www.perplexity.ai/) - Market research and news gathering
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation
- [uvicorn](https://www.uvicorn.org/) - ASGI server
- [Jinja2](https://jinja.palletsprojects.com/) - Template rendering for web interface

## 📦 Installation

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
   pip install -r requirements.txt
   # Or if using uv
   uv pip install -r requirements.txt
   ```

## ⚙️ Configuration

1. Create a `.env` file in the project root directory with the following variables:

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

   For more LLM options, refer to [documentation](https://python.langchain.com/api_reference/langchain/chat_models/langchain.chat_models.base.init_chat_model.html)

2. The application uses environment variables to configure:
   - Perplexity API for market research
   - LLM model selection and credentials

## 🚀 Usage

### API Mode

1. Start the API server:
   ```bash
   uvicorn src.agent.api.api:app --reload
   ```

   Or without auto-reload:
   ```bash
   uvicorn src.agent.api.api:app
   ```

2. The API will be available at `http://127.0.0.1:8000`

3. Access the interactive API documentation at `http://127.0.0.1:8000/docs`

4. Send analysis requests using the `/analyze` endpoint:
   ```bash
   curl -X POST "http://127.0.0.1:8000/analyze" \
      -H "Content-Type: application/json" \
      -d '{"query": "Analyze Tesla stock (TSLA) performance and financial metrics"}'
   ```

### Direct Mode

Run the application directly for interactive analysis from the command line (input query via stdin):


```bash
python src/tests/main.py
```

Follow the prompts to enter your stock analysis query.


### Interactive Web Interface

The application includes a web interface that can be accessed at `http://127.0.0.1:8000` when running in API mode. The web interface provides a user-friendly form to enter stock queries and view the analysis results in real-time.


## 📊 Multi-Agent Workflow

The system follows this workflow:

1. **Supervisor** receives the analysis query and coordinates the workflow
2. **Web Search Expert** uses Perplexity API to gather market news and trends
3. **Finance Analyst** fetches live stock prices, performance metrics, and financial data
4. **Report Generator** compiles all gathered information into a professional report
5. **Reports** are saved as markdown files in the `output/` directory

## 📁 Output Examples

Analysis reports are saved automatically in the `output/` directory with filenames following this pattern:
```
output/stock_report_{ticker}_{timestamp}.md
```

Example output files included in the repository demonstrate the format of generated reports.


## 🔧 Customization

### Prompts

The system uses customizable prompts located in `src/prompts/agent_prompts.py`:

- `WEB_SEARCH_AGENT_PROMPT` - Configuration for the web research agent
- `YAHOO_FINANCE_AGENT_PROMPT` - Configuration for the finance analyst agent
- `REPORT_GENERATOR_AGENT_PROMPT` - Configuration for the report generator agent
- `SUPERVISOR_PROMPT` - Configuration for the workflow coordinator

### Tools

Available tools in `src/tools/stock_analysis_tools.py`:

- `web_search_news` - Search for current market news and information
- `get_stock_price` - Get current stock price and basic information
- `get_stock_performance` - Get historical performance data
- `get_financial_metrics` - Get key financial metrics
- `save_report_to_file` - Save analysis reports to markdown files

### Project Configuration

The `pyproject.toml` file contains the project metadata and dependencies. The `agent_flow.json` file contains the agent workflow configuration which can be modified to change the agent behavior. The `graph.png` image is auto-generated each time the agent runs to visualize the workflow.


## 🔍 Troubleshooting

- **API Keys**: Ensure your Perplexity API key is valid and has sufficient credits
- **Internet Connectivity**: The system requires internet access for fetching financial data and market research
- **LLM Access**: Ensure your LLM API key is properly configured in the `.env` file
- **Rate Limits**: Be aware of API rate limits for both Perplexity and Yahoo Finance
- **Port Already in Use**: If port 8000 is already in use, specify a different port: `uvicorn src.agent.api.api:app --port 8001`

## 🛠️ Development Setup

For development, install the package in editable mode:

```bash
pip install -e .
```

### Running Tests

The project includes test scripts in `src/tests/` directory. You can run the interactive analysis directly to test functionality with `python src/tests/main.py` or `python src/tests/test.py` for unit tests. The application automatically generates workflow visualizations when run, which can be helpful for debugging the agent flow. 


## 📁 Directory Structure

The project is organized as follows:


- `src/agent/` - Main agent logic and FastAPI implementation
  - `src/agent/api/` - Web API endpoints and interface logic
  - `src/agent/agent.py` - Core agent workflow and supervisor setup
- `src/prompts/` - All agent system prompts in `agent_prompts.py`  
- `src/templates/` - HTML templates for the web interface in `index.html`
- `src/tests/` - Test scripts including `main.py` for interactive mode and `test.py` for unit tests
- `src/tools/` - Stock analysis tools in `stock_analysis_tools.py` with functions for market data retrieval
- `output/` - Auto-generated stock reports in markdown format
- `requirements.txt` - Production dependencies
- `pyproject.toml` - Project configuration and build metadata
- `agent_flow.json` - Agent workflow configuration
- `graph.png` - Generated workflow visualization
- `trace.png` - Debug trace visualization (if available)


## 🙏 Acknowledgments

- [LangChain](https://github.com/langchain-ai/langchain) and [LangGraph](https://github.com/langchain-ai/langgraph) for the multi-agent framework
- [yfinance](https://github.com/ranaroussi/yfinance) for financial data access
- [Perplexity](https://www.perplexity.ai/) for market research capabilities
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [Jinja2](https://jinja.palletsprojects.com/) for template rendering
