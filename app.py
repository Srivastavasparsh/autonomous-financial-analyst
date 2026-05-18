import streamlit as st
import requests
import yfinance as yf

# 1. UI Configuration (Set to Wide Mode)
st.set_page_config(page_title="AI Financial Analyst", page_icon="📈", layout="wide")

# Custom CSS for a "flashy" glowing header
st.markdown("""
    <style>
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #00C9FF, #92FE9D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .sub-header {
        color: #888888;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">Autonomous Financial Analyst</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Powered by LangGraph, Llama 3 & Live Market Data</p>', unsafe_allow_html=True)

# 2. User Input Area
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    ticker_input = st.text_input("Enter a Stock Ticker:", placeholder="e.g., NVDA, AAPL, TSLA").strip().upper()
    submit_button = st.button("Generate Intelligence Report", use_container_width=True, type="primary")

# 3. Execution Logic
if submit_button:
    if not ticker_input:
        st.warning("Please enter a valid stock ticker.")
    else:
        with st.spinner(f"Agents are actively researching {ticker_input}..."):
            try:
                # Send the request to your FastAPI backend
                response = requests.post(
                    "http://127.0.0.1:8000/analyze", 
                    json={"ticker": ticker_input}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    metrics = data.get("metrics", {})
                    
                    st.success("Analysis Complete!")
                    st.markdown("---")
                    
                    # --- FLASHY UI UPGRADES ---
                    
                    # Top Row: Beautiful Metric Cards
                    st.subheader(f"📊 {ticker_input} Live Market Data")
                    m1, m2, m3, m4 = st.columns(4)
                    
                    # Safely extract and format numbers
                    price = metrics.get('current_price', 'N/A')
                    pe = metrics.get('pe_ratio', 'N/A')
                    high = metrics.get('52_week_high', 'N/A')
                    cap = metrics.get('market_cap', 'N/A')
                    
                    m1.metric("Current Price", f"${price}" if price != 'N/A' else 'N/A')
                    m2.metric("P/E Ratio", f"{round(pe, 2)}" if isinstance(pe, (int, float)) else 'N/A')
                    m3.metric("52-Week High", f"${high}" if high != 'N/A' else 'N/A')
                    
                    # Format Market Cap to Trillions/Billions for clean reading
                    if isinstance(cap, (int, float)):
                        if cap >= 1e12:
                            cap_str = f"${cap/1e12:.2f}T"
                        elif cap >= 1e9:
                            cap_str = f"${cap/1e9:.2f}B"
                        else:
                            cap_str = f"${cap:,.0f}"
                    else:
                        cap_str = "N/A"
                    m4.metric("Market Cap", cap_str)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Middle Row: The Chart & The Report side-by-side
                    chart_col, report_col = st.columns([1, 1.5])
                    
                    with chart_col:
                        st.subheader("📈 30-Day Trend")
                        # Fetch brief history for the chart
                        stock_data = yf.Ticker(ticker_input)
                        hist = stock_data.history(period="1mo")
                        if not hist.empty:
                            st.line_chart(hist['Close'], use_container_width=True)
                        else:
                            st.info("Chart data not available.")
                            
                    with report_col:
                        st.subheader("🧠 Llama 3 Analyst Report")
                        with st.container(height=400): # Makes long reports neatly scrollable
                            st.markdown(data["report"])
                            
                else:
                    st.error(f"Backend Error: {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the backend server. Is FastAPI running?")