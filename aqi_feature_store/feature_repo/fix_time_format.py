import pandas as pd

# Load your parquet file
path = r"C:\Users\HP\Desktop\AQI predictor\aqi_feature_store\feature_repo\data\processed_unscaled.parquet"
df = pd.read_parquet(path)

# Convert 'time' to proper datetime with timezone
df["time"] = pd.to_datetime(df["time"], utc=True)

# Save back to the same file
df.to_parquet(path, index=False)

print("✅ 'time' column converted to datetime with UTC timezone and file saved!")
print(df.dtypes.head())
