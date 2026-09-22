import pandas as pd
import pandera.pandas as pa

SCHEMA = pa.DataFrameSchema({
    "event_id": pa.Column(int, unique=True, nullable=False),
    "timestamp": pa.Column(pa.DateTime, nullable=False),
    "pressure_mpa": pa.Column(float, checks=pa.Check.ge(0)),
    "injection_rate": pa.Column(float, checks=pa.Check.ge(0)),
    "magnitude": pa.Column(float, checks=pa.Check.ge(0)),
    "dt": pa.Column(float, checks=pa.Check.gt(0)),
    "future_risk_event": pa.Column(int, checks=pa.Check.isin([0, 1])),
})

def validate(path="data/generated/ae_events.parquet"):
    df = pd.read_parquet(path)
    SCHEMA.validate(df)
    assert df["timestamp"].is_monotonic_increasing
    print("Data contract: PASS")
    return df

if __name__ == "__main__":
    validate()
