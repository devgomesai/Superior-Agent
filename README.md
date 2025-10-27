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

The Superior-Agent system consists of three specialized agents coordinated by a supervisor:

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

   # LLM choice (currently only anthropic is implemented)
   LLM_CHOICE=claude-sonnet-3-5  # or another anthropic model
   ```

2. The application uses environment variables to configure:
   - Perplexity API for market research
   - LLM model selection (currently only Anthropic models are implemented)

## 🚀 Usage

### API Mode

1. Start the API server:
   ```bash
   python src/agent/api/api.py
   ```

2. The API will be available at `http://127.0.0.1:8000`

3. Send analysis requests using the `/analyze` endpoint:
   ```bash
   curl -X POST "http://127.0.0.1:8000/analyze" \
        -H "Content-Type: application/json" \
        -d '{"query": "Analyze Tesla stock (TSLA) performance and financial metrics"}'
   ```

### Direct Mode

Run the application directly for interactive analysis:

```bash
python src/tests/main.py
```

Follow the prompts to enter your stock analysis query.

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

## 🔍 Troubleshooting

- **API Keys**: Ensure your Perplexity API key is valid and has sufficient credits
- **Internet Connectivity**: The system requires internet access for fetching financial data and market research
- **LLM Access**: Ensure your Anthropic API key is properly configured if using Claude models
- **Rate Limits**: Be aware of API rate limits for both Perplexity and Yahoo Finance


### Development Setup

For development, install the package in editable mode:

```bash
pip install -e .
```


## 🙏 Acknowledgments

- [LangChain](https://github.com/langchain-ai/langchain) and [LangGraph](https://github.com/langchain-ai/langgraph) for the multi-agent framework
- [yfinance](https://github.com/ranaroussi/yfinance) for financial data access
- [Perplexity](https://www.perplexity.ai/) for market research capabilities
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
