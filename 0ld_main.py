import yfinance as yf
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.messages import SystemMessage, HumanMessage
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load the API key from the .env file
load_dotenv()

# Initialize the Llama 3 model (this is the "brain" for all our agents)
llm = ChatGroq(
    temperature=0.2, # Keep it low so the financial analysis is logical, not creative
    model_name="llama-3.1-8b-instant" 
)
from typing import TypedDict
from langgraph.graph import StateGraph, END

# Define the shared state dictionary
class AgentState(TypedDict):
    ticker: str
    news_context: str
    financial_metrics: dict
    final_report: str

def researcher_agent(state: AgentState):
    print("--- Node: Researcher Agent running ---")
    current_ticker = state.get("ticker", "Unknown")
    print(f"[*] Searching the web for real-time news on {current_ticker}...")
    
    # Use DuckDuckGo to scrape the web for the latest financial news
    search = DuckDuckGoSearchResults(num_results=3)
    news_results = search.invoke(f"{current_ticker} stock financial news")
    
    return {"news_context": f"Latest News for {current_ticker}:\n{news_results}"}

def quant_agent(state: AgentState):
    print("--- Node: Quant Agent running ---")
    current_ticker = state.get("ticker", "Unknown")
    print(f"[*] Fetching live market metrics for {current_ticker} from Yahoo Finance...")
    
    # Use yfinance to ping the live stock market
    stock = yf.Ticker(current_ticker)
    info = stock.info
    
    # Safely extract the live numbers (using .get() in case a stock is missing a metric)
    metrics = {
        "current_price": info.get("currentPrice", "N/A"),
        "pe_ratio": info.get("trailingPE", "N/A"),
        "52_week_high": info.get("fiftyTwoWeekHigh", "N/A"),
        "market_cap": info.get("marketCap", "N/A")
    }
    
    return {"financial_metrics": metrics}

from langchain_core.messages import SystemMessage, HumanMessage

def manager_agent(state: AgentState):
    print("--- Node: Manager Agent running ---")
    print("[*] Llama 3 is analyzing context and metrics...")
    
    # 1. Pull the data collected by previous nodes from the shared state
    ticker = state.get("ticker")
    news = state.get("news_context")
    metrics = state.get("financial_metrics")
    
    # 2. Design a strict system prompt to control the LLM's behavior
    system_prompt = (
        "You are an expert Wall Street financial analyst. Your job is to read the provided "
        "news context and financial metrics for a stock, and write a highly professional, concise "
        "investment report. You must provide a clear recommendation (BUY, HOLD, or SELL) with justifications."
    )
    
    # 3. Create the dynamic input message containing our actual state data
    human_prompt = f"""
    Analyze the following data for ticker symbol: {ticker}
    
    --- Market News ---
    {news}
    
    --- Financial Metrics ---
    {metrics}
    
    Please provide the final formatted report in markdown layout:
    """
    
    # 4. Invoke Llama 3 via Groq
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ])
    
    # 5. Return the LLM's generated content to update the state!
    return {"final_report": response.content}

# Initialize the graph
workflow = StateGraph(AgentState)

# Add your nodes to the workflow
workflow.add_node("researcher", researcher_agent)
workflow.add_node("quant", quant_agent)
workflow.add_node("manager", manager_agent)

# Set the flow (Edges)
workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "quant")
workflow.add_edge("quant", "manager")
workflow.add_edge("manager", END)

# Compile the app
app = workflow.compile()

if __name__ == "__main__":
    print("Starting Financial Analyst Pipeline...\n")
    
    # Define the initial state (what we start with)
    initial_state = {"ticker": "AAPL"}
    
    # Invoke the graph
    final_output = app.invoke(initial_state)
    
    # Print the result to see if the state passed through correctly!
    print("\n--- FINAL STATE ---")
    print(final_output)