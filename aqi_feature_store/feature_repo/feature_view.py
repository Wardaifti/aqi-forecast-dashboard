from datetime import timedelta
from feast import FeatureView, Field, FileSource
from feast.types import Float32
from entity import sensor  # ✅ use the defined entity

# ✅ Source file (unscaled 6-month data)
aqi_source = FileSource(
    path=r"C:\Users\HP\Desktop\AQI predictor\aqi_feature_store\feature_repo\data\processed_unscaled.parquet",
    timestamp_field="time"
)

# ✅ Feature View definition
karachi_air_features = FeatureView(
    name="karachi_air_features",
    entities=[sensor],
    ttl=timedelta(days=7),
    schema=[
        Field(name="pm10", dtype=Float32),
        Field(name="pm2_5", dtype=Float32),
        Field(name="carbon_monoxide", dtype=Float32),
        Field(name="nitrogen_dioxide", dtype=Float32),
        Field(name="sulphur_dioxide", dtype=Float32),
        Field(name="ozone", dtype=Float32),
        Field(name="temperature_2m", dtype=Float32),
        Field(name="relative_humidity_2m", dtype=Float32),
        Field(name="dew_point_2m", dtype=Float32),
        Field(name="apparent_temperature", dtype=Float32),
        Field(name="pressure_msl", dtype=Float32),
        Field(name="windspeed_10m", dtype=Float32),
        Field(name="winddirection_10m", dtype=Float32),
        Field(name="aqi", dtype=Float32),
        Field(name="aqi_change", dtype=Float32),
        Field(name="aqi_pct_change", dtype=Float32),
    ],
    online=True,
    source=aqi_source,
)
