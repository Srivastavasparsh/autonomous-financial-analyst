
"use client";
import { useState } from "react";
import ReactMarkdown from "react-markdown";
import { LineChart, Line, XAxis, Tooltip, ResponsiveContainer, YAxis } from "recharts";

export default function Home() {
// ... the rest of your code stays exactly the same
  // ==========================================
  // 1. APPLICATION STATE & API LOGIC
  // ==========================================
  const [ticker, setTicker] = useState("");
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState("");

  const analyzeStock = async () => {
    if (!ticker) return;
    setLoading(true);
    setError("");
    setData(null);

    try {
      const response = await fetch("https://fintech-ai-backend-r7w0.onrender.com", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ticker: ticker.toUpperCase() }),
      });

      if (!response.ok) throw new Error("Failed to fetch data from backend");
      
      const result = await response.json();
      setData(result);
    } catch (err: any) {
      setError(err.message || "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  // ==========================================
  // 2. DASHBOARD ARCHITECTURE (THE GRID)
  // ==========================================
  return (
    <main className="min-h-screen bg-[#070707] text-[#D1D1D1] p-6 font-sans">
      {/* Main Grid Container: 4 columns */}
      <div className="grid grid-cols-[280px_1fr_1fr_400px] gap-6 max-w-[1800px] mx-auto">

        {/* -------------------------------------- */}
        {/* COLUMN 1: LEFT SIDEBAR (Navigation)    */}
        {/* -------------------------------------- */}
       {/* -------------------------------------- */}
        {/* COLUMN 1: LEFT SIDEBAR (Navigation)    */}
        {/* -------------------------------------- */}
        <nav className="bg-[#101010] p-6 rounded-3xl space-y-8 border border-[#1A1A1A]">
            
            {/* 1. Professional Identity */}
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-cyan-400 to-emerald-400 flex items-center justify-center text-black font-extrabold text-lg">
                SS
              </div>
              <div>
                <p className="text-white font-bold text-sm tracking-wide">Sparsh Srivastava</p>
                <p className="text-xs font-medium text-emerald-400 tracking-wider uppercase mt-0.5">AI Engineer</p>
              </div>
            </div>

            {/* 2. Algorithmic Standing */}
            <div className="flex items-center gap-3 bg-[#1A1A1A] p-3 rounded-xl border border-[#222]">
                <span className="text-amber-400 text-lg">♘</span>
                <div className="flex flex-col">
                  <span className="text-xs text-white font-bold tracking-wide">LeetCode Knight</span>
                  <span className="text-[10px] text-gray-400 uppercase">Top 6% Global</span>
                </div>
            </div>

            {/* 3. Core Architecture & Projects */}
            <div className="space-y-3">
              <p className="text-[10px] uppercase text-gray-600 font-extrabold tracking-widest mb-4">Deployed Architecture</p>
              
              {/* Current Active Project */}
              <div className="bg-[#1A1A1A] text-emerald-400 px-4 py-2.5 rounded-xl text-sm font-bold shadow-sm border border-emerald-900/30 cursor-pointer flex items-center justify-between">
                <span>Autonomous Analyst</span>
                <div className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></div>
              </div>
              
              {/* Previous AI Work */}
              <div className="hover:bg-[#1A1A1A] px-4 py-2 rounded-xl text-sm text-gray-400 font-medium cursor-pointer transition-colors duration-200">
                Local-RAG-Assistant
              </div>
              <div className="hover:bg-[#1A1A1A] px-4 py-2 rounded-xl text-sm text-gray-400 font-medium cursor-pointer transition-colors duration-200">
                Smartcart-AI
              </div>
              <div className="hover:bg-[#1A1A1A] px-4 py-2 rounded-xl text-sm text-gray-400 font-medium cursor-pointer transition-colors duration-200">
                SmartBank Microservices
              </div>
            </div>

            {/* 4. Professional Experience */}
            <div className="space-y-4 pt-6 border-t border-[#1A1A1A]">
              <p className="text-[10px] uppercase text-gray-600 font-extrabold tracking-widest">Experience</p>
              
              <div className="group cursor-pointer">
                  <p className="text-sm text-gray-300 font-semibold group-hover:text-emerald-400 transition-colors">Awaaz International</p>
                  <p className="text-xs text-gray-500 font-medium mt-0.5">AI Engineer</p>
              </div>
              
              <div className="group cursor-pointer">
                  <p className="text-sm text-gray-300 font-semibold group-hover:text-emerald-400 transition-colors">VASTECH</p>
                  <p className="text-xs text-gray-500 font-medium mt-0.5">Frontend Developer</p>
              </div>
            </div>
            
        </nav>

        {/* -------------------------------------- */}
        {/* COLUMNS 2 & 3: MAIN CONTENT AREA       */}
        {/* -------------------------------------- */}
        <div className="col-span-2 space-y-6">
            
            {/* Header / Search Area */}
            <div className="flex justify-between items-center bg-[#101010] p-4 rounded-3xl border border-[#1A1A1A]">
              <div className="flex flex-1 max-w-md bg-[#0A0A0A] rounded-2xl px-4 py-2 border border-[#222]">
                <input
                  type="text"
                  value={ticker}
                  onChange={(e) => setTicker(e.target.value)}
                  placeholder="Search Ticker (e.g., NVDA)..."
                  className="bg-transparent border-none outline-none text-white w-full uppercase"
                  onKeyDown={(e) => e.key === "Enter" && analyzeStock()}
                />
              </div>
              <button 
                onClick={analyzeStock} 
                disabled={loading}
                className="bg-[#D1FF36] hover:bg-[#bce62b] text-black font-bold px-6 py-2 rounded-2xl ml-4 transition disabled:opacity-50"
              >
                {loading ? "Scanning..." : "Analyze"}
              </button>
            </div>

            {/* Error Message */}
            {error && (
              <div className="bg-red-900/20 border border-red-500/50 text-red-400 p-4 rounded-2xl text-center">
                {error}
              </div>
            )}

            {/* Results Area */}
            {data && data.metrics && (
              <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-700">
                
                {/* Metric Cards */}
                <div className="grid grid-cols-4 gap-4">
                  {[
                    { label: "Price", value: `$${data.metrics.current_price}` },
                    { label: "P/E Ratio", value: data.metrics.pe_ratio ? Number(data.metrics.pe_ratio).toFixed(2) : "N/A" },
                    { label: "52W High", value: `$${data.metrics["52_week_high"]}` },
                    { label: "Market Cap", value: `$${(data.metrics.market_cap / 1e9).toFixed(2)}B` }
                  ].map((metric, i) => (
                    <div key={i} className="bg-[#101010] border border-[#1A1A1A] p-5 rounded-3xl shadow-lg">
                      <p className="text-gray-500 text-xs font-semibold uppercase tracking-wider mb-2">{metric.label}</p>
                      <p className="text-xl font-bold text-white">{metric.value}</p>
                    </div>
                  ))}
                </div>
                {/* 30-Day Trend Chart */}
                {data.chart && data.chart.length > 0 && (
                  <div className="bg-[#101010] border border-[#1A1A1A] p-6 rounded-3xl shadow-lg h-72">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-gray-400 text-sm font-bold uppercase tracking-wider">30-Day Price Trend</h3>
                      <span className="text-xs text-emerald-400 bg-emerald-400/10 px-2 py-1 rounded">Live Data</span>
                    </div>
                    <ResponsiveContainer width="100%" height="80%">
                      <LineChart data={data.chart}>
                        <XAxis dataKey="date" stroke="#555" fontSize={12} tickLine={false} axisLine={false} minTickGap={20} />
                        <YAxis domain={['auto', 'auto']} hide />
                        <Tooltip
                          contentStyle={{ backgroundColor: '#1A1A1A', borderColor: '#333', borderRadius: '12px', color: '#fff' }}
                          itemStyle={{ color: '#D1FF36', fontWeight: 'bold' }}
                          labelStyle={{ color: '#888', marginBottom: '4px' }}
                        />
                        <Line 
                          type="monotone" 
                          dataKey="price" 
                          stroke="#D1FF36" 
                          strokeWidth={3} 
                          dot={false} 
                          activeDot={{ r: 6, fill: '#D1FF36', stroke: '#101010', strokeWidth: 2 }}
                        />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                )}

                {/* AI Report Container */}
                <div className="bg-[#101010] border border-[#1A1A1A] rounded-3xl p-8 shadow-lg">
                  <div className="flex items-center gap-2 mb-6 pb-4 border-b border-[#222]">
                    <div className="w-2 h-2 rounded-full bg-[#D1FF36] animate-pulse"></div>
                    <h3 className="text-white font-bold text-lg">Llama 3 Intelligence Report</h3>
                  </div>
                  <div className="prose prose-invert max-w-none text-sm text-gray-300">
                    <ReactMarkdown>{data.report}</ReactMarkdown>
                  </div>
                </div>

              </div>
            )}
        </div>

        {/* -------------------------------------- */}
        {/* COLUMN 4: RIGHT SIDEBAR (Tools)        */}
        {/* -------------------------------------- */}
        <aside className="bg-[#101010] p-6 rounded-3xl space-y-6 border border-[#1A1A1A]">
            <h3 className="text-white font-bold mb-4">Position Calculator</h3>
            <div className="bg-[#0A0A0A] p-4 rounded-2xl border border-[#222] space-y-4">
              <div>
                <label className="text-xs text-gray-500 uppercase font-bold">Account Size ($)</label>
                <input type="text" placeholder="10,000" className="w-full bg-[#1A1A1A] border border-[#333] rounded-lg mt-1 p-2 text-white" disabled />
              </div>
              <div>
                <label className="text-xs text-gray-500 uppercase font-bold">Risk %</label>
                <input type="text" placeholder="2%" className="w-full bg-[#1A1A1A] border border-[#333] rounded-lg mt-1 p-2 text-white" disabled />
              </div>
              <button className="w-full bg-[#333] text-gray-400 py-2 rounded-lg font-bold text-sm cursor-not-allowed">Calculate (Coming Soon)</button>
            </div>
            
            <div className="mt-8">
               <h3 className="text-white font-bold mb-4">System Status</h3>
               <div className="flex items-center justify-between bg-[#0A0A0A] p-4 rounded-2xl border border-[#222]">
                  <span className="text-sm text-gray-400">LLM Inference</span>
                  <span className="text-emerald-400 text-xs font-bold bg-emerald-400/10 px-2 py-1 rounded">Online</span>
               </div>
            </div>
        </aside>

      </div>
    </main>
  );
}