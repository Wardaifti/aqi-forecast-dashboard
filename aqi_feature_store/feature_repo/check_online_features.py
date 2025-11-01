from feast import FeatureStore

store = FeatureStore(repo_path=".")
df = store.get_online_features(
    features=[
        "karachi_air_features:pm10",
        "karachi_air_features:pm2_5",
        "karachi_air_features:aqi",
    ],
    entity_rows=[{"sensor_id": "KHI_SENSOR_1"}]
).to_df()

print(df.head())
