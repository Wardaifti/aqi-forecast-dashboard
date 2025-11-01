import pandas as pd

# ✅ Path to your existing CSV
csv_path = r"C:\Users\HP\Desktop\AQI predictor\aqi_feature_store\feature_repo\data\processed_karachi_unscaled copy.csv"

# ✅ Path where we’ll save the Parquet file
parquet_path = r"C:\Users\HP\Desktop\AQI predictor\aqi_feature_store\feature_repo\data\processed_unscaled.parquet"

# ✅ Read the CSV
df = pd.read_csv(csv_path)

# ✅ Save as Parquet
df.to_parquet(parquet_path, index=False)

print("✅ Conversion complete! File saved at:", parquet_path)
