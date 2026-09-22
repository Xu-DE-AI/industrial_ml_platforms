"""
Iceberg learning lab.

For a real Iceberg catalog:
    Spark/Flink -> Iceberg table -> object storage -> catalog

This file keeps a local fallback so the project is runnable without a cloud account.
"""

from pathlib import Path
import pandas as pd

def create_local_lake():
    src = Path("data/generated/ae_events.parquet")
    out = Path("lakehouse/bronze")
    out.mkdir(parents=True, exist_ok=True)

    df = pd.read_parquet(src)
    df["ingest_date"] = df["timestamp"].dt.date.astype(str)
    df.to_parquet(out/"events.parquet", index=False)

    print("Created local bronze table.")
    print("""
Production Iceberg exercises:
1. CREATE TABLE ... USING iceberg
2. INSERT INTO
3. MERGE INTO for idempotent upserts
4. ALTER TABLE ADD COLUMN for schema evolution
5. inspect snapshots
6. query an older snapshot
7. compact small files
8. partition by ingest_date / region
""")

if __name__ == "__main__":
    create_local_lake()
