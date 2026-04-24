import { useEffect, useState } from "react";
import {
  analyzeText,
  uploadCSV,
  getStats,
  getTrend,
  getTopAspects
} from "../api";

import Sidebar from "../layout/Sidebar";
import SentimentPieChart from "../components/SentimentPieChart";
import AspectBarChart from "../components/AspectBarChart";
import TrendChart from "../components/TrendChart";
import TopAspects from "../components/TopAspects";

function Dashboard() {
  const [category, setCategory] = useState("phones");
  const [stats, setStats] = useState([]);
  const [trend, setTrend] = useState([]);
  const [topAspects, setTopAspects] = useState({});
  const [input, setInput] = useState("");
  const [file, setFile] = useState(null);

  const loadData = async (cat) => {
    setStats(await getStats(cat));
    setTrend(await getTrend(cat));
    setTopAspects(await getTopAspects(cat));
  };

  useEffect(() => {
    loadData(category);
  }, [category]);

  const handleAnalyze = async () => {
    await analyzeText(input, category);
    setInput("");
    loadData(category);
  };

  const handleUpload = async () => {
    await uploadCSV(file);
    loadData(category);
  };

  // KPI counts
  const total = stats.length;
  const positive = stats.filter(s => s.sentiment === "positive").length;
  const negative = stats.filter(s => s.sentiment === "negative").length;

  return (
    <div className="layout">

      {/* SIDEBAR */}
      <Sidebar category={category} setCategory={setCategory} />

      {/* MAIN */}
      <div className="main">

        {/* TOP BAR */}
        <div className="top-bar">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Enter review..."
          />
          <button onClick={handleAnalyze}>Analyze</button>

          <input type="file" onChange={(e) => setFile(e.target.files[0])} />
          <button onClick={handleUpload}>Upload</button>
        </div>

        {/* KPI CARDS */}
        <div className="kpi-row">
          <div className="kpi-card">Total Reviews: {total}</div>
          <div className="kpi-card positive">Positive: {positive}</div>
          <div className="kpi-card negative">Negative: {negative}</div>
        </div>

        {/* CHART GRID */}
        <div className="grid">

          <div className="card hover">
            <h3>Sentiment</h3>
            <SentimentPieChart data={stats} />
          </div>

          <div className="card hover">
            <h3>Aspect Analysis</h3>
            <AspectBarChart data={stats.slice(0, 10)} />
          </div>

          <div className="card hover">
            <h3>Trend</h3>
            <TrendChart data={trend} />
          </div>

          <div className="card hover">
            <h3>Top Aspects</h3>
            <TopAspects data={topAspects} />
          </div>

        </div>
      </div>
    </div>
  );
}

export default Dashboard;