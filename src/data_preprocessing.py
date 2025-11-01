import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib
import logging

# CONFIG
RAW_DATA_PATH = "data/raw/karachi_merged_data.csv"
PROCESSED_UNSCALED = "data/processed/processed_karachi_unscaled.csv"
PROCESSED_SCALED = "data/processed/processed_karachi_scaled.csv"
SCALER_PATH = "data/models/scaler.joblib"

LAG_FEATURES = [1, 2, 3]
ROLL_WINDOWS = [3, 6, 24]
NUMERIC_FEATURES = [
    "pm10", "pm2_5", "carbon_monoxide", "nitrogen_dioxide",
    "sulphur_dioxide", "ozone", "temperature_2m", "relative_humidity_2m",
    "apparent_temperature", "pressure_msl", "surface_pressure",
    "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"
]

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# -------------------------------
# AQI CALCULATION 
# -------------------------------
def compute_aqi(df):
    def calc_subindex(conc, breakpoints):
        for (low, high, ilow, ihigh) in breakpoints:
            if low <= conc <= high:
                return ((ihigh - ilow) / (high - low)) * (conc - low) + ilow
        return None

    # Breakpoints
    bp_pm25 = [(0,30,0,50),(31,60,51,100),(61,90,101,200),(91,120,201,300),(121,250,301,400),(251,350,401,500)]
    bp_pm10 = [(0,50,0,50),(51,100,51,100),(101,250,101,200),(251,350,201,300),(351,430,301,400),(431,600,401,500)]
    bp_no2  = [(0,40,0,50),(41,80,51,100),(81,180,101,200),(181,280,201,300),(281,400,301,400),(401,1000,401,500)]
    bp_so2  = [(0,40,0,50),(41,80,51,100),(81,380,101,200),(381,800,201,300),(801,1600,301,400),(1601,2600,401,500)]
    bp_co   = [(0,1,0,50),(1.1,2,51,100),(2.1,10,101,200),(10.1,17,201,300),(17.1,34,301,400),(34.1,50,401,500)]
    bp_o3   = [(0,50,0,50),(51,100,51,100),(101,168,101,200),(169,208,201,300),(209,748,301,400),(749,1000,401,500)]

    aqi_values = []
    for _, row in df.iterrows():
        subs = []
        if pd.notna(row.get("pm2_5")):
            subs.append(calc_subindex(row["pm2_5"], bp_pm25))
        if pd.notna(row.get("pm10")):
            subs.append(calc_subindex(row["pm10"], bp_pm10))
        if pd.notna(row.get("nitrogen_dioxide")):
            subs.append(calc_subindex(row["nitrogen_dioxide"], bp_no2))
        if pd.notna(row.get("sulphur_dioxide")):
            subs.append(calc_subindex(row["sulphur_dioxide"], bp_so2))
        if pd.notna(row.get("carbon_monoxide")):
            subs.append(calc_subindex(row["carbon_monoxide"] / 1000, bp_co))
        if pd.notna(row.get("ozone")):
            subs.append(calc_subindex(row["ozone"], bp_o3))

        subs = [s for s in subs if s is not None]
        aqi_values.append(max(subs) if subs else np.nan)

    df["aqi"] = aqi_values
    logging.info("✅ AQI column computed successfully.")
    return df

# -------------------------------
# PREPROCESSING STEPS 
# -------------------------------
def to_datetime_index(df, ts_col="time"):
    df[ts_col] = pd.to_datetime(df[ts_col], errors="coerce")
    df = df.sort_values(ts_col)
    df.set_index(ts_col, inplace=True)
    return df

def impute_missing(df):
    df.replace("", np.nan, inplace=True)
    df = df.ffill().bfill()
    df = df.interpolate(method="time", limit_direction="both")
    for c in df.columns:
        if df[c].isna().any():
            df[c].fillna(df[c].median(), inplace=True)
    return df

def cap_outliers_iqr(df):
    for col in NUMERIC_FEATURES + ["aqi"]:
        if col in df.columns:
            Q1, Q3 = df[col].quantile(0.25), df[col].quantile(0.75)
            IQR = Q3 - Q1
            df[col] = df[col].clip(Q1 - 1.5*IQR, Q3 + 1.5*IQR)
    return df

def add_time_features(df):
    df["hour"] = df.index.hour
    df["day"] = df.index.day
    df["month"] = df.index.month
    df["year"] = df.index.year
    df["weekday"] = df.index.weekday
    df["is_weekend"] = df["weekday"].isin([5,6]).astype(int)
    return df

def add_aqi_change(df):
    if "aqi" in df.columns:
        df["aqi_change"] = df["aqi"].diff()
        df["aqi_pct_change"] = df["aqi"].pct_change().replace([np.inf, -np.inf], np.nan).fillna(0)
    return df

def add_lags_and_rolls(df):
    for col in ["aqi"]:
        for lag in LAG_FEATURES:
            df[f"{col}_lag{lag}"] = df[col].shift(lag)
        for w in ROLL_WINDOWS:
            df[f"{col}_roll{w}"] = df[col].rolling(window=w, min_periods=1).mean()
    return df

# -------------------------------
# SAVE OUTPUTS
# -------------------------------
def save_outputs(df):
    os.makedirs(os.path.dirname(PROCESSED_UNSCALED), exist_ok=True)
    os.makedirs(os.path.dirname(PROCESSED_SCALED), exist_ok=True)
    os.makedirs(os.path.dirname(SCALER_PATH), exist_ok=True)

    df_reset = df.reset_index()
    df_reset.to_csv(PROCESSED_UNSCALED, index=False)
    logging.info(f"💾 Unscaled data saved: {PROCESSED_UNSCALED}")

    numeric_cols = [c for c in df_reset.columns if df_reset[c].dtype in [np.float64, np.int64]]
    scaler = StandardScaler()
    df_scaled = df_reset.copy()
    df_scaled[numeric_cols] = scaler.fit_transform(df_scaled[numeric_cols])
    df_scaled.to_csv(PROCESSED_SCALED, index=False)
    joblib.dump(scaler, SCALER_PATH)

    logging.info(f"💾 Scaled data saved: {PROCESSED_SCALED}")
    logging.info(f"📁 Scaler saved: {SCALER_PATH}")

# -------------------------------
# WRAPPED FUNCTION for pipeline
# -------------------------------
def preprocess_data(df):
    """
    Preprocess and feature engineer the input DataFrame.
    Can be called directly from main_pipeline.py
    """
    logging.info("🚀 Starting preprocessing + feature engineering pipeline...")
    logging.info(f"Initial data shape: {df.shape}")

    df = to_datetime_index(df, ts_col="time")
    df = impute_missing(df)
    df = compute_aqi(df)
    df = cap_outliers_iqr(df)
    df = add_time_features(df)
    df = add_aqi_change(df)
    df = add_lags_and_rolls(df)

    df.dropna(inplace=True)
    save_outputs(df)

    logging.info(f"✅ Preprocessing complete. Final shape: {df.shape}")
    return df

# Standalone mode (run independently)
if __name__ == "__main__":
    df_raw = pd.read_csv(RAW_DATA_PATH)
    preprocess_data(df_raw)
