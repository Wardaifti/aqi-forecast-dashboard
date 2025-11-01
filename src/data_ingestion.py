import requests
import pandas as pd
from datetime import datetime, timedelta
import os

CITY = "Karachi"
LAT, LON = 24.8607, 67.0011
OUTPUT_FILE = "data/raw/karachi_merged_data.csv"
DAYS = 180  # 6 months


def fetch_openmeteo_aqi(days=DAYS):
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=days)
    url = (
        "https://air-quality-api.open-meteo.com/v1/air-quality?"
        f"latitude={LAT}&longitude={LON}"
        f"&hourly=pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone"
        f"&start_date={start_date}&end_date={end_date}"
        f"&timezone=Asia/Karachi"
    )
    print(f"📅 Fetching AIR QUALITY data from {start_date} to {end_date}...")
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"❌ AQI API request failed: {response.status_code} — {response.text}")
    data = response.json()
    hourly = data.get("hourly", {})
    if not hourly:
        print("⚠️ No hourly air-quality data available.")
        return None
    df_aqi = pd.DataFrame(hourly)
    print(f"✅ Retrieved {len(df_aqi)} hourly air-quality records.")
    return df_aqi


def fetch_weather_data(days=DAYS):
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=days)
    url = (
        "https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={LAT}&longitude={LON}"
        f"&hourly=temperature_2m,relative_humidity_2m,dew_point_2m,"
        f"apparent_temperature,pressure_msl,windspeed_10m,winddirection_10m"
        f"&start_date={start_date}&end_date={end_date}"
        f"&timezone=Asia/Karachi"
    )
    print(f"📅 Fetching WEATHER data from {start_date} to {end_date}...")
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"❌ Weather API request failed: {response.status_code} — {response.text}")
    data = response.json()
    hourly = data.get("hourly", {})
    if not hourly:
        print("⚠️ No hourly weather data available.")
        return None
    df_weather = pd.DataFrame(hourly)
    print(f"✅ Retrieved {len(df_weather)} hourly weather records.")
    return df_weather


def save_to_csv(df, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, index=False)
    print(f"💾 Data saved to {filepath}")


def ingest_data(days=DAYS):
    """Main function to ingest, merge, and save AQI + weather data."""
    df_aqi = fetch_openmeteo_aqi(days)
    df_weather = fetch_weather_data(days)
    if df_aqi is not None and df_weather is not None:
        df_merged = pd.merge(df_aqi, df_weather, on="time", how="inner")
        print(f"✅ Merged dataset shape: {df_merged.shape}")
        save_to_csv(df_merged, OUTPUT_FILE)
        print("✅ Data ingestion and merging complete!")
        return df_merged
    else:
        print("⚠️ Missing one of the datasets, merge skipped.")
        return None


if __name__ == "__main__":
    ingest_data()
