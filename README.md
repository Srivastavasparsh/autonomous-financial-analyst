# 📈 Autonomous Financial Analyst AI

![Next.js](https://img.shields.io/badge/Next.js-black?style=for-the-badge&logo=next.js&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangGraph-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)

A full-stack, multi-agent AI architecture designed to automate financial research. This application utilizes a decoupled Next.js frontend and a FastAPI backend to orchestrate autonomous AI agents that scrape live market data, analyze web news, and generate professional investment reports in real-time.

## 🚀 System Architecture

This project utilizes the **Full-Stack AI** pattern, separating the inference engine (Brain) from the user interface (Face) for maximum scalability.

* **The Frontend (React/Next.js):** A highly responsive, dark-mode dashboard styled with Tailwind CSS and Recharts for live data visualization.
* **The Backend (FastAPI):** A high-performance REST API that acts as the gateway to the AI inference engine.
* **The AI Engine (LangGraph + Llama 3):** A deterministic state graph containing three specialized agents:
  1. **Researcher Agent:** Scrapes real-time financial news via DuckDuckGo.
  2. **Quant Agent:** Pulls live market caps, P/E ratios, and historical pricing via Yahoo Finance.
  3. **Manager Agent:** An ultra-low latency Llama 3 LLM (via Groq) that synthesizes the data into a Markdown-formatted investment thesis.

## ⚡ Live Demo
* **Frontend:** [Insert your Vercel URL here]
* **Backend API:** [Insert your Render URL here]

## 🛠️ Local Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/autonomous-financial-analyst.git](https://github.com/your-username/autonomous-financial-analyst.git)
cd autonomous-financial-analyst