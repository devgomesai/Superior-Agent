#  ** Exmaple Test **
# from IPython.display import Image, display
# from langchain_anthropic import ChatAnthropic
# from dotenv import load_dotenv
# from langgraph_supervisor import create_supervisor
# from langchain.agents import create_agent
# from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod, NodeStyles
# import os
# import yfinance as yf
# try:
#     from ..prompts.agent_prompts import WEB_SEARCH_AGENT_PROMPT, SUPERVISOR_PROMPT, YAHOO_FINANCE_AGENT_PROMPT, REPORT_GENERATOR_AGENT_PROMPT
# except ImportError:
#     import sys
#     import os
#     sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#     from prompts.agent_prompts import WEB_SEARCH_AGENT_PROMPT, SUPERVISOR_PROMPT, YAHOO_FINANCE_AGENT_PROMPT, REPORT_GENERATOR_AGENT_PROMPT
# from datetime import datetime, timedelta
# import requests
# import json

# # Load environment variables
# load_dotenv()

# os.makedirs("output", exist_ok=True)

# # Initialize model
# model = ChatAnthropic(model=os.getenv("LLM_CHOICE"))
# perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")


# # Define tools for Web Search Agent
# def web_search_news(query: str) -> str:
#     """Search the web for current news and information about stocks using Perplexity API."""
#     try:
#         url = "https://api.perplexity.ai/chat/completions"
        
#         headers = {
#             "Authorization": f"Bearer {perplexity_api_key}",
#             "Content-Type": "application/json",
#         }
        
#         payload = {
#             "model": "sonar-pro",
#             "messages": [
#                 {
#                     "role": "user",
#                     "content": f"Search for and provide current information about: {query}. Include recent news, market trends, analyst opinions, competitive landscape, growth catalysts, and relevant risks. Provide comprehensive details suitable for institutional investment analysis."
#                 }
#             ],
#             "temperature": 0.7,
#             "top_p": 0.9,
#             "return_images": False,
#             "return_related_questions": False,
#         }
        
#         response = requests.post(url, headers=headers, json=payload, timeout=30)
#         response.raise_for_status()
        
#         result = response.json()
#         content = result["choices"][0]["message"]["content"]
        
#         return f"Perplexity Search Results for '{query}':\n{content}"
#     except Exception as e:
#         return f"Error searching with Perplexity: {str(e)}"


# # Define tools for Yahoo Finance Agent
# def get_stock_price(ticker: str) -> str:
#     """Get current stock price and basic info for a ticker."""
#     try:
#         stock = yf.Ticker(ticker)
#         data = stock.history(period="1d")
#         info = stock.info
        
#         if data.empty:
#             return f"No data found for ticker: {ticker}"
        
#         current_price = data['Close'].iloc[-1]
#         return (
#             f"Stock: {ticker}\n"
#             f"Current Price: ${current_price:.2f}\n"
#             f"Market Cap: ${info.get('marketCap', 'N/A')}\n"
#             f"P/E Ratio: {info.get('trailingPE', 'N/A')}\n"
#             f"Forward P/E: {info.get('forwardPE', 'N/A')}\n"
#             f"52-Week High: ${info.get('fiftyTwoWeekHigh', 'N/A')}\n"
#             f"52-Week Low: ${info.get('fiftyTwoWeekLow', 'N/A')}\n"
#             f"Average Volume: {info.get('averageVolume', 'N/A')}"
#         )
#     except Exception as e:
#         return f"Error fetching data for {ticker}: {str(e)}"


# def get_stock_performance(ticker: str, period: str = "1y") -> str:
#     """Get historical performance data for a stock."""
#     try:
#         stock = yf.Ticker(ticker)
#         hist = stock.history(period=period)
        
#         if hist.empty:
#             return f"No historical data found for {ticker}"
        
#         start_price = hist['Close'].iloc[0]
#         end_price = hist['Close'].iloc[-1]
#         change_percent = ((end_price - start_price) / start_price) * 100
        
#         return (
#             f"Stock Performance for {ticker} ({period}):\n"
#             f"Start Price: ${start_price:.2f}\n"
#             f"End Price: ${end_price:.2f}\n"
#             f"Change: {change_percent:.2f}%\n"
#             f"High: ${hist['High'].max():.2f}\n"
#             f"Low: ${hist['Low'].min():.2f}\n"
#             f"Average Price: ${hist['Close'].mean():.2f}\n"
#             f"Volatility (Std Dev): {hist['Close'].std():.2f}"
#         )
#     except Exception as e:
#         return f"Error fetching performance data for {ticker}: {str(e)}"


# def get_financial_metrics(ticker: str) -> str:
#     """Get key financial metrics for a stock."""
#     try:
#         stock = yf.Ticker(ticker)
#         info = stock.info
        
#         metrics = {
#             'Revenue (TTM)': info.get('totalRevenue', 'N/A'),
#             'Net Income (TTM)': info.get('netIncomeToCommon', 'N/A'),
#             'Operating Income': info.get('operatingCashflow', 'N/A'),
#             'Free Cash Flow': info.get('freeCashflow', 'N/A'),
#             'Gross Profit Margin': f"{info.get('grossMargins', 'N/A')}%" if info.get('grossMargins') else 'N/A',
#             'Operating Margin': f"{info.get('operatingMargins', 'N/A')}%" if info.get('operatingMargins') else 'N/A',
#             'Net Profit Margin': f"{info.get('profitMargins', 'N/A')}%" if info.get('profitMargins') else 'N/A',
#             'ROE (Return on Equity)': f"{info.get('returnOnEquity', 'N/A')}%" if info.get('returnOnEquity') else 'N/A',
#             'ROA (Return on Assets)': f"{info.get('returnOnAssets', 'N/A')}%" if info.get('returnOnAssets') else 'N/A',
#             'Debt to Equity': info.get('debtToEquity', 'N/A'),
#             'Current Ratio': info.get('currentRatio', 'N/A'),
#             'Quick Ratio': info.get('quickRatio', 'N/A'),
#             'Dividend Yield': f"{info.get('dividendYield', 'N/A')}%" if info.get('dividendYield') else 'N/A',
#             'Payout Ratio': f"{info.get('payoutRatio', 'N/A')}%" if info.get('payoutRatio') else 'N/A',
#             'Beta': info.get('beta', 'N/A'),
#             'EPS (Trailing)': info.get('trailingEps', 'N/A'),
#             'EPS (Forward)': info.get('forwardEps', 'N/A'),
#             'PEG Ratio': info.get('pegRatio', 'N/A'),
#             'Book Value Per Share': info.get('bookValue', 'N/A'),
#         }
        
#         result = f"Financial Metrics for {ticker}:\n"
#         for metric, value in metrics.items():
#             result += f"{metric}: {value}\n"
        
#         return result
#     except Exception as e:
#         return f"Error fetching financial metrics for {ticker}: {str(e)}"


# def save_report_to_file(report_content: str, ticker: str) -> str:
#     """Save the stock analysis report to a markdown file."""
#     try:
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         filename = f"output/stock_report_{ticker}_{timestamp}.md"
        
#         with open(filename, 'w', encoding='utf-8') as f:
#             f.write(report_content)
        
#         return f"Report successfully saved to {filename}"
#     except Exception as e:
#         return f"Error saving report: {str(e)}"


# # Create specialized agents
# web_search_agent = create_agent(
#     model=model,
#     tools=[web_search_news],
#     name="web_search_expert",
#     system_prompt=WEB_SEARCH_AGENT_PROMPT,
# )

# yahoo_finance_agent = create_agent(
#     model=model,
#     tools=[get_stock_price, get_stock_performance, get_financial_metrics],
#     name="finance_analyst",
#     system_prompt=YAHOO_FINANCE_AGENT_PROMPT,
# )

# report_generator_agent = create_agent(
#     model=model,
#     tools=[save_report_to_file],
#     name="report_generator",
#     system_prompt=REPORT_GENERATOR_AGENT_PROMPT,
# )

# # Create supervisor workflow
# workflow = create_supervisor(
#     agents=[web_search_agent, yahoo_finance_agent, report_generator_agent],
#     model=model,
#     prompt=SUPERVISOR_PROMPT
# )    

# def main():
#     # Compile the workflow
#     app = workflow.compile()

#     # Draw and save graph as PNG
#     graph_image = app.get_graph().draw_mermaid_png(
#         curve_style=CurveStyle.LINEAR,
#         node_colors=NodeStyles(
#             first="#FF6B6B",  # Vibrant red for start
#             last="#4ECDC4",  # Teal for end
#             default="#95E1D3",  # Mint green for regular nodes
#         ),
#         wrap_label_n_words=9,
#         output_file_path='graph.png',
#         background_color="white",
#         padding=20,
#     )
    
#     user_input = input("Enter Query: ")
    
#     # Run analysis
#     print(f"\n🔍 Generating comprehensive stock analysis for {user_input}...")
#     print("=" * 80)
    
#     result = app.invoke(
#         {
#             "messages": [
#                 {
#                     "role": "user",
#                     "content": user_input
#                 }
#             ]
#         }
#     )

#     print("\n--- Stock Analysis Complete ---\n")
#     for m in result['messages']:
#         print(m.pretty_print())
    
#     print("\n" + "=" * 80)
#     print("✅ Report generation complete! Check the 'output' folder for the saved markdown file.")


# if __name__ == "__main__":
#     main()