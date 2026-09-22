import pandas as pd
from quality.schema import SCHEMA

def main():
    df = pd.read_parquet("data/generated/reservoir.parquet")
    SCHEMA.validate(df)
    assert df["timestamp"].is_monotonic_increasing
    assert not df.duplicated(["timestamp", "well_id"]).any()
    print("Reservoir data quality: PASS")

if __name__ == "__main__":
    main()
