-- Run against a Spark session configured with Iceberg.
-- This is intentionally a reference implementation.

CREATE TABLE IF NOT EXISTS lake.ae_events (
    event_id BIGINT,
    timestamp TIMESTAMP,
    sensor_id STRING,
    region STRING,
    pressure_mpa DOUBLE,
    injection_rate DOUBLE,
    magnitude DOUBLE,
    dt DOUBLE,
    z_fault_normal DOUBLE,
    future_risk_event INT
)
USING iceberg
PARTITIONED BY (days(timestamp), region);

-- Idempotent ingestion pattern
MERGE INTO lake.ae_events t
USING incoming_events s
ON t.event_id = s.event_id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;

-- Schema evolution
ALTER TABLE lake.ae_events ADD COLUMN source_version STRING;

-- Time travel depends on the catalog/table history:
-- SELECT * FROM lake.ae_events VERSION AS OF 123;
