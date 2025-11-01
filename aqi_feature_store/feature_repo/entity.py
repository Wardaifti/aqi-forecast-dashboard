from feast import Entity, ValueType

# Define a simple entity for each record (matches the column name sensor_id)
sensor = Entity(
    name="sensor_id",             # ✅ same as the join key & column name
    join_keys=["sensor_id"],      # ✅ this stays the same
    description="Unique identifier for AQI sensor record",
    value_type=ValueType.STRING
)
