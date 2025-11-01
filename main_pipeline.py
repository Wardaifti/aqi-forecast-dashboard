from src.data_ingestion import ingest_data
from src.data_preprocessing import preprocess_data
from src.feature_store_update import update_feast_store   # 👈 new import

def main():
    print("🚀 Starting AQI pipeline...")

    # Step 1: Data Ingestion
    df_raw = ingest_data()

    # Step 2: Data Preprocessing
    df_cleaned = preprocess_data(df_raw)

    # Step 3: Update Feast Feature Store
    print("📦 Sending processed data to Feast feature store...")
    update_feast_store(df_cleaned)

    print("✅ Pipeline complete! All steps executed successfully.")

if __name__ == "__main__":
    main()
