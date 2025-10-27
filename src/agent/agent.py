from langchain_anthropic import ChatAnthropic
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langgraph_supervisor import create_supervisor
from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod, NodeStyles
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
# model = ChatAnthropic(model=os.getenv("LLM_CHOICE"), temperature=0.1)
model = ChatGroq(model=os.getenv("LLM_CHOICE"),
                 temperature=0.1,
                 api_key=os.getenv("GROQ_API_KEY"))


# Create specialized agents
web_search_agent = create_agent(
    model=model,
    tools=[web_search_news],
    name="web_search_agent",
    system_prompt=WEB_SEARCH_AGENT_PROMPT,
)

yahoo_finance_agent = create_agent(
    model=model,
    tools=[get_stock_price, get_stock_performance, get_financial_metrics],
    name="finacial_yf_agent",
    system_prompt=YAHOO_FINANCE_AGENT_PROMPT,
)

report_generator_agent = create_agent(
    model=model,
    tools=[save_report_to_file],
    name="report_generator_agent",
    system_prompt=REPORT_GENERATOR_AGENT_PROMPT,
)

# Create supervisor workflow
workflow = create_supervisor(
    agents=[web_search_agent, yahoo_finance_agent, report_generator_agent],
    model=model,
    prompt=SUPERVISOR_PROMPT,
    supervisor_name="financial_manager_agent"
    
)    

def get_agent():
    """Get the compiled agent application"""
    app = workflow.compile()
    try:
        app.get_graph().draw_mermaid_png(
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
        
    return app
