from langchain_anthropic import ChatAnthropic
# from langchain_ollama import ChatOllama
from dotenv import load_dotenv
from langgraph_supervisor import create_supervisor
from langchain.agents import create_agent
import os

os.makedirs("output", exist_ok=True)

try:
    from ..tools.stock_analysis_tools import (
    web_search_news,
    get_stock_price,
    get_stock_performance,
    get_financial_metrics,
    save_report_to_file
)
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from tools.stock_analysis_tools import (
    web_search_news,
    get_stock_price,
    get_stock_performance,
    get_financial_metrics,
    save_report_to_file
)
    
try:
    from ..prompts.agent_prompts import (
    WEB_SEARCH_AGENT_PROMPT,
    YAHOO_FINANCE_AGENT_PROMPT,
    REPORT_GENERATOR_AGENT_PROMPT,
    SUPERVISOR_PROMPT
    )
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from prompts.agent_prompts import (
    WEB_SEARCH_AGENT_PROMPT,
    YAHOO_FINANCE_AGENT_PROMPT,
    REPORT_GENERATOR_AGENT_PROMPT,
    SUPERVISOR_PROMPT
)



load_dotenv()

# Initialize model
model = ChatAnthropic(model=os.getenv("LLM_CHOICE"))
# model = ChatOllama(model="qwen3:0.6b", temperature=0) # not better tool calling

# Create specialized agents

web_search_agent = create_agent(
    model=model,
    tools=[web_search_news],
    name="web_search_expert",
    system_prompt=WEB_SEARCH_AGENT_PROMPT,
)

yahoo_finance_agent = create_agent(
    model=model,
    tools=[get_stock_price, get_stock_performance, get_financial_metrics],
    name="finance_analyst",
    system_prompt=YAHOO_FINANCE_AGENT_PROMPT,
)

report_generator_agent = create_agent(
    model=model,
    tools=[save_report_to_file],
    name="report_generator",
    system_prompt=REPORT_GENERATOR_AGENT_PROMPT,
)

# Create supervisor workflow
workflow = create_supervisor(
    agents=[web_search_agent, yahoo_finance_agent, report_generator_agent],
    model=model,
    prompt=SUPERVISOR_PROMPT
)    

def get_agent():
    """Get the compiled agent application"""
    app = workflow.compile()
    return app
