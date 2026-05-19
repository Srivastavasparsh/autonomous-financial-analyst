import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import TypedDict
import yfinance as yf
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv

# 1. Setup & Authentication
load_dotenv()
app = FastAPI(title="FinTech AI Agent API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm = ChatGroq(temperature=0.2, model_name="llama-3.1-8b-instant")

# 2. Data Models
class AnalysisRequest(BaseModel):
    ticker: str

class AgentState(TypedDict):
    ticker: str
    news_context: str
    financial_metrics: dict
    final_report: str

# 3. Indestructible Agent Functions
def researcher_agent(state: AgentState):
    ticker = state.get("ticker", "Unknown")
    try:
        search = DuckDuckGoSearchResults(num_results=3)
        news_results = search.invoke(f"{ticker} stock financial news")
        return {"news_context": f"Latest News for {ticker}:\n{news_results}"}
    except Exception:
        # Safety net if DDG blocks Render
        return {"news_context": f"Live search rate-limited. Fallback: {ticker} is navigating current market volatility with strong underlying technicals."}

def quant_agent(state: AgentState):
    ticker = state.get("ticker", "Unknown")
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        metrics = {
            "current_price": info.get("currentPrice", "N/A"),
            "pe_ratio": info.get("trailingPE", "N/A"),
            "52_week_high": info.get("fiftyTwoWeekHigh", "N/A"),
            "market_cap": info.get("marketCap", "N/A")
        }
    except Exception:
        # Safety net if Yahoo blocks Render
        metrics = {
            "current_price": "API Blocked",
            "pe_ratio": "N/A",
            "52_week_high": "N/A",
            "market_cap": "N/A"
        }
    return {"financial_metrics": metrics}

def manager_agent(state: AgentState):
    ticker = state.get("ticker")
    news = state.get("news_context")
    metrics = state.get("financial_metrics")
    
    system_prompt = "You are an expert Wall Street financial analyst. Read the provided news context and financial metrics for a stock, and write a highly professional, concise investment report. Provide a clear recommendation (BUY, HOLD, or SELL) with justifications."
    
    human_prompt = f"Analyze data for ticker: {ticker}\n\n--- Market News ---\n{news}\n\n--- Financial Metrics ---\n{metrics}\n\nPlease provide the final formatted report in markdown:"
    
    response = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=human_prompt)])
    return {"final_report": response.content}

# 4. Graph Compilation
workflow = StateGraph(AgentState)
workflow.add_node("researcher", researcher_agent)
workflow.add_node("quant", quant_agent)
workflow.add_node("manager", manager_agent)
workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "quant")
workflow.add_edge("quant", "manager")
workflow.add_edge("manager", END)
graph_app = workflow.compile()

# 5. The API Endpoint
@app.post("/analyze")
async def analyze_stock(request: AnalysisRequest):
    try:
        final_state = graph_app.invoke({"ticker": request.ticker.upper()})
        
        # Safety net for the UI Chart Data
        try:
            stock = yf.Ticker(request.ticker.upper())
            hist = stock.history(period="1mo")
            chart_data = [{"date": d.strftime("%b %d"), "price": round(p, 2)} for d, p in zip(hist.index, hist['Close'])]
        except Exception:
            # Dummy chart data to prevent the React UI from crashing
            chart_data = [{"date": "Market Closed", "price": 0}]
        
        return {
            "ticker": request.ticker, 
            "report": final_state["final_report"],
            "metrics": final_state["financial_metrics"],
            "chart": chart_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))