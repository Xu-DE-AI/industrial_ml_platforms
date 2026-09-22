from pathlib import Path
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from prometheus_client import Counter, Histogram, make_asgi_app
import time

MODEL = Path("artifacts/geothermal_risk_model.joblib")
app = FastAPI(title="Geothermal Risk API", version="1.0.0")

REQUESTS = Counter("risk_requests_total", "Total predictions")
LATENCY = Histogram("risk_prediction_seconds", "Prediction latency")

class ReservoirRequest(BaseModel):
    injection_rate: float = Field(ge=0)
    pressure_mpa: float = Field(ge=0)
    temperature_c: float
    flow_rate: float = Field(ge=0)
    seismic_rate: float = Field(ge=0)
    seismic_distance_km: float = Field(ge=0)
    pressure_mpa_mean_1d: float = Field(ge=0)
    injection_rate_mean_1d: float = Field(ge=0)
    seismic_rate_mean_1d: float = Field(ge=0)
    pressure_change_6h: float
    injection_change_6h: float

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/ready")
def ready():
    if not MODEL.exists():
        raise HTTPException(503, "model not loaded")
    return {"status": "ready"}

@app.post("/predict")
def predict(req: ReservoirRequest):
    REQUESTS.inc()
    t = time.perf_counter()

    if not MODEL.exists():
        raise HTTPException(503, "model unavailable")

    model = joblib.load(MODEL)
    x = pd.DataFrame([req.model_dump()])
    p = float(model.predict_proba(x)[0, 1])

    LATENCY.observe(time.perf_counter() - t)
    return {
        "risk_probability": p,
        "decision_threshold": 0.50,
        "model_version": "registered-model",
    }

app.mount("/metrics", make_asgi_app())
