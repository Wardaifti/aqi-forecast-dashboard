from flask import Flask, jsonify, request
import pandas as pd
import joblib
import requests
import numpy as np
from datetime import datetime, timedelta, date
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# ----------------------------- #
# Load trained AQI prediction model
# ----------------------------- #


MODEL_PATH = os.path.join(os.path.dirname(__file__), "aqi_feature_store", "rf_aqi_model.pkl")
model = joblib.load(MODEL_PATH)


# ----------------------------- #
# Fetch past 7 days pollutant data
# ----------------------------- #
def fetch_past_7_days_air_quality(lat=24.8607, lon=67.0011):
    end_date = date.today()
    start_date = end_date - timedelta(days=7)
    
    try:
        url = (
            f"https://air-quality-api.open-meteo.com/v1/air-quality?"
            f"latitude={lat}&longitude={lon}"
            f"&start_date={start_date}&end_date={end_date}"
            "&hourly=pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone"
        )
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            hourly_data = {key: data["hourly"].get(key, [0]) for key in ["pm10","pm2_5","carbon_monoxide","nitrogen_dioxide","sulphur_dioxide","ozone"]}
            daily_averages = {key: [] for key in hourly_data.keys()}
            for i in range(7):
                for key, values in hourly_data.items():
                    start_idx = i*24
                    end_idx = start_idx + 24
                    day_values = values[start_idx:end_idx] if len(values) >= end_idx else values[start_idx:]
                    daily_averages[key].append(round(float(np.mean(day_values)), 2) if day_values else 0)
            return daily_averages
    except Exception as e:
        print("Open-Meteo error:", e)

    # Backup: OpenAQ API
    try:
        url = (
            f"https://api.openaq.org/v3/measurements?"
            f"coordinates={lat},{lon}&radius=10000&limit=1000"
            f"&date_from={start_date}&date_to={end_date}"
        )
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            records = []
            for rec in data.get("results", []):
                if rec.get("parameter") in ["pm10","pm25","co","no2","so2","o3"]:
                    records.append({"parameter": rec.get("parameter"), "value": rec.get("value")})
            if records:
                df = pd.DataFrame(records)
                daily_averages = {}
                mapping = {"pm10":"pm10","pm25":"pm2_5","co":"carbon_monoxide","no2":"nitrogen_dioxide","so2":"sulphur_dioxide","o3":"ozone"}
                for key, mapped in mapping.items():
                    daily_averages[mapped] = [round(float(df[df["parameter"]==key]["value"].mean()), 2)]*7
                return daily_averages
    except Exception as e:
        print("OpenAQ backup error:", e)

    # Fallback: zeros
    print("❌ Failed to fetch past pollutant data.")
    return {k:[0]*7 for k in ["pm10","pm2_5","carbon_monoxide","nitrogen_dioxide","sulphur_dioxide","ozone"]}

# ----------------------------- #
# Predict AQI for next 3 days using trend + dust awareness
# ----------------------------- #
def predict_future_aqi(daily_averages):
    pollutants = ["pm10","pm2_5","carbon_monoxide","nitrogen_dioxide","sulphur_dioxide","ozone"]
    trend = {}
    last_day_avg = {}
    for p in pollutants:
        trend[p] = daily_averages[p][-1] - daily_averages[p][-2] if len(daily_averages[p])>=2 else 0
        last_day_avg[p] = daily_averages[p][-1]

    # 🌫️ Dust-awareness boost (small, realistic multiplier for Day 1)
    pm25 = last_day_avg["pm2_5"]
    pm10 = last_day_avg["pm10"]
    dust_factor = 1.0
    if pm25 > 80 or pm10 > 150:
        dust_factor = 1.2
    elif pm25 > 50 or pm10 > 100:
        dust_factor = 1.15
    elif pm25 > 35 or pm10 > 70:
        dust_factor = 1.1

    print(f"🌫️ PM2.5={pm25}, PM10={pm10}, Day 1 Dust factor={dust_factor}")

    predictions = []
    for i in range(1, 4):
        future_features = np.array([last_day_avg[p] + trend[p]*i for p in pollutants])
        padded_features = np.pad(future_features, (0, 15 - len(future_features)), 'constant').reshape(1, -1)

        predicted_aqi = model.predict(padded_features)[0]

        # Apply dust factor only for Day 1
        if i == 1:
            predicted_aqi = round(float(predicted_aqi * dust_factor), 2)
        else:
            predicted_aqi = round(float(predicted_aqi), 2)

        date_str = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
        predictions.append({"date":date_str, "day":f"Day {i}", "predicted_AQI":predicted_aqi})

    current_pollutants = {p: round(float(last_day_avg[p]),2) for p in pollutants}
    return current_pollutants, predictions

# ----------------------------- #
# Main Forecast Endpoint (returns current + past + predictions)
# ----------------------------- #
@app.route("/forecast", methods=["GET"])
def forecast():
    city = request.args.get("city","Karachi")
    lat = float(request.args.get("lat",24.8607))
    lon = float(request.args.get("lon",67.0011))

    daily_averages = fetch_past_7_days_air_quality(lat, lon)
    current_pollutants, predictions = predict_future_aqi(daily_averages)

    return jsonify({
        "city": city,
        "pollutants": current_pollutants,
        "pollutants_history": daily_averages,
        "predictions": predictions,
        "note": "Day 1 prediction adjusted for realistic dust conditions"
    })

# ----------------------------- #
# Run Flask App
# ----------------------------- #
# ----------------------------- #
# Run Flask App
# ----------------------------- #
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Railway provides PORT env var
    app.run(host="0.0.0.0", port=port)
