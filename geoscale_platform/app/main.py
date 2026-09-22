from pathlib import Path
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from prometheus_client import Counter, Histogram, make_asgi_app

MODEL_PATH = Path("artifacts/risk_model.joblib")

app = FastAPI(title="GeoScale Risk API", version="1.0.0")
REQUESTS = Counter("prediction_requests_total", "Prediction requests")
LATENCY = Histogram("prediction_latency_seconds", "Prediction latency")

class Request(BaseModel):
    pressure_mpa: float = Field(ge=0)
    injection_rate: float = Field(ge=0)
    magnitude: float = Field(ge=0)
    dt: float = Field(gt=0)
    z_fault_normal: float

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/ready")
def ready():
    if not MODEL_PATH.exists():
        raise HTTPException(503, "model unavailable")
    return {"status": "ready"}

@app.post("/predict")
def predict(req: Request):
    import time
    REQUESTS.inc()
    t = time.perf_counter()

    if not MODEL_PATH.exists():
        raise HTTPException(503, "model unavailable")

    model = joblib.load(MODEL_PATH)
    x = pd.DataFrame([req.model_dump()])
    probability = float(model.predict_proba(x)[0, 1])

    LATENCY.observe(time.perf_counter() - t)
    return {"risk_probability": probability, "model_version": "local"}

app.mount("/metrics", make_asgi_app())
