import pandas as pd

path = r"C:\Users\HP\Desktop\AQI predictor\aqi_feature_store\feature_repo\data\processed_unscaled.parquet"

df = pd.read_parquet(path)

# ✅ Create the column if it doesn't exist
if 'sensor_id' not in df.columns:
    df['sensor_id'] = "KHI_SENSOR_1"

# ✅ Ensure it's string type
df['sensor_id'] = df['sensor_id'].astype(str)

# ✅ Save back to parquet
df.to_parquet(path, index=False)

print("✅ sensor_id column is now present and string type in parquet.")
