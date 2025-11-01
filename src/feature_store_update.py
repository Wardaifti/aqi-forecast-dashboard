from feast import FeatureStore
from datetime import datetime
import os
import pandas as pd

def update_feast_store(processed_df):
    print("🚀 Updating Feast feature store...")

    # ✅ Always find the correct path to feature_repo
    script_dir = os.path.dirname(os.path.abspath(__file__))
    feast_repo_path = os.path.abspath(os.path.join(script_dir, "..", "aqi_feature_store"))

    store = FeatureStore(repo_path=feast_repo_path)

    # ✅ Ensure Feast’s required columns exist
    if "event_timestamp" not in processed_df.columns:
        processed_df = processed_df.reset_index().rename(columns={"time": "event_timestamp"})

    # ✅ Add static entity key (you can later make this dynamic)
    processed_df["location_id"] = "karachi"

    # ✅ Save data locally for Feast’s offline store
    offline_path = "data/feast_data/karachi_features.parquet"
    os.makedirs(os.path.dirname(offline_path), exist_ok=True)
    processed_df.to_parquet(offline_path, index=False)

    # ✅ Apply feature definitions and materialize to online store
    store.apply(store.repo_path)
    store.materialize_incremental(end_date=datetime.now())

    print("✅ Feast feature store updated successfully!")
