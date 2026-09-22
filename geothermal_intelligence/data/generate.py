from pathlib import Path
import numpy as np
import pandas as pd

OUT = Path("data/generated")
OUT.mkdir(parents=True, exist_ok=True)

def main():
    rng = np.random.default_rng(11)
    n = 100_000
    ts = pd.date_range("2025-01-01", periods=n, freq="15min")

    well = rng.choice(["W01", "W02", "W03", "W04"], n)
    injection = np.clip(100 + 20*np.sin(np.arange(n)/500) + rng.normal(0, 8, n), 0, None)
    pressure = 80 + .08*injection + rng.normal(0, 3, n)
    temperature = 180 + rng.normal(0, 2, n)
    flow = np.clip(60 + .4*injection + rng.normal(0, 5, n), 0, None)
    seismic_rate = np.clip(
        .02*np.exp(.025*(pressure-80)) + rng.normal(0, .01, n), 0, None
    )
    distance = np.abs(rng.normal(4, 5, n))

    latent = (
        .03*(pressure-80)
        + .02*(injection-100)
        + 1.2*seismic_rate
        - .03*distance
        + rng.normal(0, 1, n)
    )

    # Rare future-event label.
    threshold = np.quantile(latent, .985)
    target = (latent > threshold).astype(int)

    df = pd.DataFrame({
        "timestamp": ts,
        "well_id": well,
        "injection_rate": injection,
        "pressure_mpa": pressure,
        "temperature_c": temperature,
        "flow_rate": flow,
        "seismic_rate": seismic_rate,
        "seismic_distance_km": distance,
        "future_seismic_event_6h": target,
    })

    df.to_parquet(OUT/"reservoir.parquet", index=False)
    print(f"Wrote {len(df):,} rows")

if __name__ == "__main__":
    main()
