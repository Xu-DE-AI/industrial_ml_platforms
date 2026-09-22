from pathlib import Path
import pandas as pd

def test_feature_dataset():
    path = Path("data/generated/gold_features.parquet")
    if not path.exists():
        return
    df = pd.read_parquet(path)
    assert "future_seismic_event_6h" in df
    assert not df.empty
    assert df["timestamp"].is_monotonic_increasing
