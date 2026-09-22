from pathlib import Path
import numpy as np
import pandas as pd

OUT = Path("data/generated")
OUT.mkdir(parents=True, exist_ok=True)

def main():
    rng = np.random.default_rng(7)
    n = 150_000

    ts = pd.date_range("2026-01-01", periods=n, freq="min")
    sensor = rng.choice([f"S{i:02d}" for i in range(1, 33)], n)
    region = rng.choice(["fault_zone", "far_field", "well_A", "well_B"], n)
    pressure = 20 + np.linspace(0, 90, n) + rng.normal(0, 2, n)
    injection = np.clip(10 + 3*np.sin(np.arange(n)/3000) + rng.normal(0, 1, n), 0, None)
    magnitude = np.clip(.4 + .25*np.log1p(pressure) + rng.normal(0, .12, n), .05, None)
    dt = rng.lognormal(-1.0, .7, n)
    z = np.where(region == "fault_zone", rng.normal(0, 3, n), rng.normal(0, 15, n))

    # Future-event label with temporal dependence.
    risk_score = (
        .035*pressure + .08*injection + .15*magnitude
        - .025*np.abs(z) + rng.normal(0, 1.5, n)
    )
    future_event = (risk_score > np.quantile(risk_score, .985)).astype(int)

    df = pd.DataFrame({
        "event_id": np.arange(n, dtype=np.int64),
        "timestamp": ts,
        "sensor_id": sensor,
        "region": region,
        "pressure_mpa": pressure,
        "injection_rate": injection,
        "magnitude": magnitude,
        "dt": dt,
        "z_fault_normal": z,
        "future_risk_event": future_event,
    })

    df.to_parquet(OUT/"ae_events.parquet", index=False)
    print(f"Wrote {len(df):,} events")

if __name__ == "__main__":
    main()
