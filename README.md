# 🌤️ AQI Forecast Dashboard  

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/Backend-Flask-green)
![React](https://img.shields.io/badge/Frontend-React-blue)
![CI/CD](https://img.shields.io/badge/Automation-GitHub%20Actions-yellow)
![License](https://img.shields.io/badge/License-MIT-purple)

---

## 📘 Overview  

**AQI Forecast Dashboard** is an end-to-end **Air Quality Index (AQI) prediction system** built using a fully **serverless machine learning pipeline**.  
It predicts the **AQI for the next 3 days** in your city using real-time weather and pollutant data from open APIs.  

The project automates **data ingestion, preprocessing, feature engineering, model training, feature storage, CI/CD, and real-time visualization** via a modern web dashboard.

---

## 🧠 Features  

<details>
<summary><b>📊 Data Pipeline</b></summary>

- Fetches 6 months of historical weather and pollutant data from Open Meteo APIs.  
- Merges pollutant and weather data into a single dataset automatically.  
- Stores raw, cleaned, and feature-engineered data separately.  
</details>

<details>
<summary><b>⚙️ Preprocessing & Feature Engineering</b></summary>

- Computes AQI from pollutant concentrations using official breakpoints.  
- Handles missing values and caps outliers.  
- Adds **time-based**, **lag**, **rolling**, and **rate-of-change** features.  
- Standardizes and stores both scaled and unscaled datasets.  
</details>

<details>
<summary><b>📦 Feature Store (Feast)</b></summary>

- Stores engineered features with timestamps and entity keys.  
- Supports offline training and online inference feature retrieval.  
</details>

<details>
<summary><b>🤖 Machine Learning</b></summary>

- Trained **Random Forest** and **XGBoost** models for AQI prediction.  
- Evaluated with RMSE, MAE, and R² metrics.  
- Achieved exceptional accuracy:  

Mean Squared Error (MSE): 1.85
Root Mean Squared Error (RMSE): 1.36
Mean Absolute Error (MAE): 0.29
R² Score: 1.00

</details>

<details>
<summary><b>🧩 CI/CD & Automation</b></summary>

- GitHub Actions handle hourly data ingestion and daily model retraining.  
- Continuous deployment using Railway for backend and Netlify for frontend.  
</details>

<details>
<summary><b>💻 Web Dashboard</b></summary>

- Built with **React** + **Flask**.  
- Displays:
- Current AQI via animated gauge.
- Past 7-day pollutant trends.  
- 3-day AQI forecast cards.  
- Uses **Recharts** for dynamic graphs.  
</details>

<details>
<summary><b>🧾 Explainability (SHAP)</b></summary>

- Visualizes feature importance for model transparency.  
</details>

---

## 🏗️ Architecture  

```mermaid
graph TD;
  A[Open Meteo APIs] --> B[Data Ingestion]
  B --> C[Preprocessing + Feature Engineering]
  C --> D[Feast Feature Store]
  D --> E[Model Training (RandomForest / XGBoost)]
  E --> F[Model Registry + GitHub Actions (CI/CD)]
  F --> G[Flask Backend API]
  G --> H[React Frontend Dashboard]

🧩 Tech Stack
Layer	Technologies
Data Collection	Python, Open Meteo API
Preprocessing	Pandas, NumPy, Scikit-learn
Feature Store	Feast
Modeling	Random Forest, XGBoost
Explainability	SHAP
Backend	Flask, REST API
Frontend	React, Recharts, GaugeChart
CI/CD	GitHub Actions
Deployment	Railway

aqi-forecast-dashboard/
│
├── data/
│   ├── raw/                  # Raw API data
│   ├── processed/            # Cleaned and feature-engineered data
│   └── models/               # Scaler + trained model files
│
├── feature_repo/             # Feast feature definitions
├── aqi_feature_store/        # Feature registry
│
├── frontend/                 # React frontend
│
├── data_ingestion.py         # Fetch and merge data
├── preprocessing.py          # Preprocessing + feature engineering
├── app.py                    # Flask backend (API)
├── requirements.txt          # Dependencies
└── README.md                 # You are here!

🚀 Getting Started
1️⃣ Clone Repository
git clone https://github.com/Wardaifti/aqi-forecast-dashboard.git
cd aqi-forecast-dashboard

2️⃣ Setup Virtual Environment
python -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)
pip install -r requirements.txt

3️⃣ Run Data Pipeline
python data_ingestion.py
python preprocessing.py

4️⃣ Start Backend
python app.py

5️⃣ Launch Frontend
cd frontend
npm install
npm start


Then open → http://localhost:3000

📊 Sample Output

Model Performance:

MSE: 1.85  
RMSE: 1.36  
MAE: 0.29  
R²: 1.00


Dashboard Features:
🌡️ Real-time AQI Gauge
📈 Past Trends Visualization
🔮 3-Day Forecast Predictions
⚠️ Dust-Aware Adjustments

🧭 Future Enhancements

Add LSTM / Transformer-based deep models for AQI forecasting.

Enable multi-city prediction and regional alerting.

Introduce notifications (email/SMS) for hazardous levels.

Expand feature store for real-time ingestion.

👩‍💻 Author

Warda Iftikhar
🎓 DUET’25 | AI & Machine Learning Engineer
💡 Aspiring Data Scientist 

📬 Connect with me on LinkedIn: https://www.linkedin.com/in/warda-iftikhar-791310258/

