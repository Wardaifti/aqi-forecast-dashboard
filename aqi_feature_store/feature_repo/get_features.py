from feast import FeatureStore
import pandas as pd

if __name__ == "__main__":
    # Initialize the feature store
    store = FeatureStore(repo_path=".")

    # ✅ Create entity rows that match your Entity definition
    # sensor_id must be STRING and match the one in your parquet file ("KHI_SENSOR_1")
    entity_df = pd.DataFrame({
        "sensor_id": ["KHI_SENSOR_1"]
    })

    # ✅ Retrieve features from the online store
    features = store.get_online_features(
        features=[
            "karachi_air_features:pm2_5",
            "karachi_air_features:pm10",
            "karachi_air_features:carbon_monoxide",
            "karachi_air_features:nitrogen_dioxide",
        ],
        entity_rows=entity_df.to_dict(orient="records"),
    ).to_dict()

    print("✅ Retrieved features:")
    for key, value in features.items():
        print(f"{key}: {value}")
