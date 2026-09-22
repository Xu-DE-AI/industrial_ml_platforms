import pandas as pd

BASE = [
    "injection_rate", "pressure_mpa", "temperature_c",
    "flow_rate", "seismic_rate", "seismic_distance_km"
]

def main():
    df = pd.read_parquet("data/generated/reservoir.parquet").sort_values(
        ["well_id", "timestamp"]
    )

    for c in ["pressure_mpa", "injection_rate", "seismic_rate"]:
        df[f"{c}_mean_1d"] = (
            df.groupby("well_id")[c]
            .transform(lambda s: s.rolling(96, min_periods=10).mean())
        )

    # Critical: all features are lagged. No information from the current/future
    # prediction horizon is allowed to leak into the feature vector.
    df["pressure_change_6h"] = (
        df.groupby("well_id")["pressure_mpa"].diff(24)
    )
    df["injection_change_6h"] = (
        df.groupby("well_id")["injection_rate"].diff(24)
    )

    features = BASE + [
        "pressure_mpa_mean_1d",
        "injection_rate_mean_1d",
        "seismic_rate_mean_1d",
        "pressure_change_6h",
        "injection_change_6h",
    ]

    df[features + ["timestamp", "well_id", "future_seismic_event_6h"]].dropna().to_parquet(
        "data/generated/gold_features.parquet", index=False
    )

if __name__ == "__main__":
    main()
