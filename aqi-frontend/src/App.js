import React, { useEffect, useState } from "react";
import GaugeChart from "react-gauge-chart";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  BarChart,
  Bar,
} from "recharts";
import "./App.css";

function App() {
  const [activeTab, setActiveTab] = useState("dashboard");
  const [data, setData] = useState(null);
  const [importanceData, setImportanceData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Load AQI forecast data
  useEffect(() => {
  const backendUrl =
    process.env.NODE_ENV === "production"
      ? "https://aqi-forecast-dashboard-production.up.railway.app/forecast"
      : "http://127.0.0.1:8080/forecast";

  fetch(backendUrl)
    .then((res) => {
      if (!res.ok) throw new Error("Failed to fetch backend data");
      return res.json();
    })
    .then((data) => setData(data))
    .catch((err) => setError(err.message))
    .finally(() => setLoading(false));
}, []);


  // Load SHAP importance data
  useEffect(() => {
    fetch("/feature_importance.json")
      .then((res) => res.json())
      .then((json) => setImportanceData(json))
      .catch((err) => console.error("Feature importance load error:", err));
  }, []);

  const getAQIColor = (aqi) => {
    if (aqi <= 50) return "#2ecc71";
    if (aqi <= 100) return "#f1c40f";
    if (aqi <= 150) return "#e67e22";
    if (aqi <= 200) return "#e74c3c";
    if (aqi <= 300) return "#8e44ad";
    return "#7E0023";
  };

  if (loading) return <h2>Loading Air Quality Data...</h2>;
  if (error) return <h2>Error: {error}</h2>;

  const pollutants = data.pollutants_history || {};
  const pastDays = Array.from({ length: 7 }, (_, i) => `Day ${i + 1}`);
  const pollutantChartData = pastDays.map((day, i) => ({
    day,
    PM2_5: pollutants.pm2_5?.[i],
    PM10: pollutants.pm10?.[i],
    CO: pollutants.carbon_monoxide?.[i],
    NO2: pollutants.nitrogen_dioxide?.[i],
    SO2: pollutants.sulphur_dioxide?.[i],
    O3: pollutants.ozone?.[i],
  }));

  const avgAQI =
    data.predictions.reduce((sum, p) => sum + p.predicted_AQI, 0) /
    data.predictions.length;
  const normalizedAQI = Math.min(avgAQI / 500, 1);

  return (
    <div className="app">
      {/* Header */}
      <header className="app-header">
        <h1>🌤 Karachi Air Quality Dashboard</h1>
        <p>AI-Driven AQI Forecast & Analytics</p>
      </header>

      {/* Tabs */}
      <div className="tabs">
        <button
          className={activeTab === "dashboard" ? "active" : ""}
          onClick={() => setActiveTab("dashboard")}
        >
          Dashboard
        </button>
        <button
          className={activeTab === "analytics" ? "active" : ""}
          onClick={() => setActiveTab("analytics")}
        >
          Analytics
        </button>
      </div>

      {/* Dashboard Tab */}
      {activeTab === "dashboard" && (
        <>
          {/* Main Grid Section */}
          <div className="main-grid">
            <div className="gauge-section">
              <h3>🌡️ Current AQI Status</h3>
              <GaugeChart
                id="aqi-gauge"
                nrOfLevels={6}
                colors={[
                  "#2ecc71",
                  "#f1c40f",
                  "#e67e22",
                  "#e74c3c",
                  "#8e44ad",
                  "#7E0023",
                ]}
                arcWidth={0.3}
                percent={normalizedAQI}
                textColor="#fff"
                formatTextValue={() => `${Math.round(avgAQI)} AQI`}
              />
              <p
                style={{
                  color: getAQIColor(avgAQI),
                  fontWeight: "bold",
                  marginTop: "10px",
                }}
              >
                {avgAQI <= 50
                  ? "Good 😊"
                  : avgAQI <= 100
                  ? "Moderate 😐"
                  : avgAQI <= 150
                  ? "Unhealthy for Sensitive Groups 😷"
                  : avgAQI <= 200
                  ? "Unhealthy 😷"
                  : avgAQI <= 300
                  ? "Very Unhealthy ☠️"
                  : "Hazardous ☠️"}
              </p>
            </div>

            <div className="chart-section">
              <h3>📈 Past 7 Days Pollutant Trends</h3>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={pollutantChartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="day" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="PM2_5" stroke="#FF5733" strokeWidth={2} />
                  <Line type="monotone" dataKey="PM10" stroke="#33C1FF" strokeWidth={2} />
                  <Line type="monotone" dataKey="CO" stroke="#FFC300" strokeWidth={2} />
                  <Line type="monotone" dataKey="NO2" stroke="#900C3F" strokeWidth={2} />
                  <Line type="monotone" dataKey="SO2" stroke="#2ecc71" strokeWidth={2} />
                  <Line type="monotone" dataKey="O3" stroke="#8E44AD" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Forecast Cards */}
          <div className="forecast-section">
            {data.predictions.map((p, index) => (
              <div
                key={index}
                className="forecast-card"
                style={{ borderTop: `5px solid ${getAQIColor(p.predicted_AQI)}` }}
              >
                <h4>{p.day}</h4>
                <p>{p.date}</p>
                <h3>{p.predicted_AQI.toFixed(1)}</h3>
                <span style={{ color: getAQIColor(p.predicted_AQI) }}>
                  {p.predicted_AQI <= 50
                    ? "Good"
                    : p.predicted_AQI <= 100
                    ? "Moderate"
                    : p.predicted_AQI <= 150
                    ? "Unhealthy (SG)"
                    : p.predicted_AQI <= 200
                    ? "Unhealthy"
                    : p.predicted_AQI <= 300
                    ? "Very Unhealthy"
                    : "Hazardous"}
                </span>
              </div>
            ))}
          </div>
        </>
      )}

      {/* Analytics Tab */}
      {activeTab === "analytics" && (
  <div className="analytics-section">
    <h3>📊 Feature Importance (SHAP Analysis)</h3>
    <ResponsiveContainer width="90%" height={400}>
      <BarChart data={importanceData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="Feature" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="Importance" fill="#1abc9c" />
      </BarChart>
    </ResponsiveContainer>

    {/* --- New Model Performance Section --- */}
    <div className="model-metrics">
      <h3>🤖 Model Performance Summary</h3>
      <div className="metric-grid">
        <div className="metric-card">
          <h4>R² Score</h4>
          <p>0.99</p>
        </div>
        <div className="metric-card">
          <h4>RMSE</h4>
          <p>2.24</p>
        </div>
        <div className="metric-card">
          <h4>MAE</h4>
          <p>0.52</p>
        </div>
        <div className="metric-card">
          <h4>MSE</h4>
          <p>5.02</p>
        </div>
      </div>
      <p className="metric-note">
        ✅ Random Forest model evaluated with excellent performance — near-perfect fit for current AQI forecast data.
      </p>
    </div>
  </div>
)}

      

      <footer className="footer">
        <p>Developed with ❤️ using Flask + React</p>
      </footer>
    </div>
  );
}

export default App;
