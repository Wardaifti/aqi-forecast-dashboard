import pandas as pd

path = r"C:\Users\HP\Desktop\AQI predictor\aqi_feature_store\feature_repo\data\processed_unscaled.parquet"

# Add sensor_id
df = pd.read_parquet(path)
df["sensor_id"] = "KHI_SENSOR_1"
df.to_parquet(path, index=False)
print("✅ sensor_id added to parquet file at Feast path.")

# Verify immediately
df = pd.read_parquet(path)
print("\nColumns now present in parquet file:")
print(df.columns)
