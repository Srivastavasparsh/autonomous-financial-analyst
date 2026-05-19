import os
import yfinance as yf
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import TypedDict, Dict, Any, List
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv

# ==========================================
# 1. Configuration & Setup
# ==========================================
load_dotenv()

app = FastAPI(
    title="Autonomous Financial Analyst API",
    description="AI Agent for generating real-time stock reports.",
    version="1.0.0"
)

# The Bridge: Allows your Next.js frontend to talk to this server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For strict security later, replace "*" with your Vercel URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the LLM (Requires GROQ_API_KEY in environment)
llm = ChatGroq(temperature=0.2, model_name="llama-3.1-8b-instant")

# ==========================================
# 2. Data Structures
# ==========================================
class AnalysisRequest(BaseModel):
    ticker: str

class AgentState(TypedDict):
    ticker: str
    news_context: str
    financial_metrics: Dict[str, Any]
    final_report: str

# ==========================================
# 3. Agent Tooling (With Graceful Fallbacks)
# ==========================================
def fetch_news_context(ticker: str) -> str:
    """Safely fetches market news, bypassing rate limits if necessary."""
    try:
        search = DuckDuckGoSearchResults(num_results=3)
        results = search.invoke(f"{ticker} stock financial news market")
        return f"Latest News for {ticker}:\n{results}"
    except Exception as e:
        print(f"Search warning: {e}")
        return f"Live search unavailable. Fallback Context: {ticker} is navigating current market volatility. Analysts emphasize monitoring underlying technicals and upcoming earnings reports."

def fetch_financial_metrics(ticker: str) -> Dict[str, Any]:
    """Safely fetches Yahoo Finance data, protecting against cloud IP blocks."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            "current_price": info.get("currentPrice", "Data Unavailable"),
            "pe_ratio": info.get("trailingPE", "N/A"),
            "52_week_high": info.get("fiftyTwoWeekHigh", "N/A"),
            "market_cap": info.get("marketCap", "N/A")
        }
    except Exception as e:
        print(f"YFinance warning: {e}")
        return {
            "current_price": "API Blocked",
            "pe_ratio": "N/A",
            "52_week_high": "N/A",
            "market_cap": "N/A"
        }

def fetch_chart_data(ticker: str) -> List[Dict[str, Any]]:
    """Safely fetches 30-day historical data for the UI chart."""
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1mo")
        return [{"date": d.strftime("%b %d"), "price": round(p, 2)} for d, p in zip(hist.index, hist['Close'])]
    except Exception:
        return [{"date": "Market Closed", "price": 0}]

# ==========================================
# 4. LangGraph Nodes
# ==========================================
def researcher_agent(state: AgentState):
    ticker = state.get("ticker", "Unknown")
    news = fetch_news_context(ticker)
    return {"news_context": news}

def quant_agent(state: AgentState):
    ticker = state.get("ticker", "Unknown")
    metrics = fetch_financial_metrics(ticker)
    return {"financial_metrics": metrics}

def manager_agent(state: AgentState):
    ticker = state.get("ticker")
    news = state.get("news_context")
    metrics = state.get("financial_metrics")
    
    system_prompt = """You are an expert Wall Street financial analyst. 
    Read the provided news context and financial metrics for a stock, and write a highly professional, concise investment report. 
    Provide a clear recommendation (BUY, HOLD, or SELL) with justifications. Format entirely in Markdown."""
    
    human_prompt = f"Analyze data for ticker: {ticker}\n\n--- Market News ---\n{news}\n\n--- Financial Metrics ---\n{metrics}"
    
    response = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=human_prompt)])
    return {"final_report": response.content}

# ==========================================
# 5. Graph Compilation
# ==========================================
workflow = StateGraph(AgentState)
workflow.add_node("researcher", researcher_agent)
workflow.add_node("quant", quant_agent)
workflow.add_node("manager", manager_agent)

workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "quant")
workflow.add_edge("quant", "manager")
workflow.add_edge("manager", END)

graph_app = workflow.compile()

# ==========================================
# 6. API Routing
# ==========================================
@app.post("/analyze")
async def analyze_stock(request: AnalysisRequest):
    """Main endpoint to trigger the autonomous analyst."""
    clean_ticker = request.ticker.upper().strip()
    
    try:
        # Trigger the AI graph
        final_state = graph_app.invoke({"ticker": clean_ticker})
        
        # Grab UI-specific chart data
        chart_data = fetch_chart_data(clean_ticker)
        
        return {
            "ticker": clean_ticker, 
            "report": final_state["final_report"],
            "metrics": final_state["financial_metrics"],
            "chart": chart_data
        }
    except Exception as e:
        # If the whole graph crashes, send a clean 500 error back to React
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")