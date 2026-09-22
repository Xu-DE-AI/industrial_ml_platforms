## Problem

Predict whether abnormal seismicity will occur in the next 6 hours while maintaining
safe reservoir operations.

## Architecture

```text
well + seismic telemetry
          |
        Kafka
          |
     Bronze lakehouse
          |
     data quality
          |
     Silver tables
          |
        Spark
          |
     Gold features
          |
     +----+----+
     |         |
   Feast     MLflow
     |         |
 online      registry
 features       |
     |           |
     +-----+-----+
           |
       XGBoost
           |
     calibration
           |
        FastAPI
           |
      Kubernetes
           |
   Prometheus/Grafana
           |
      drift alerts
```

## ML design

Target:
`future_seismic_event_6h`

Metrics:
- PR-AUC
- ROC-AUC
- recall
- precision
- F1
- Brier score
- calibration error

Validation:
- chronological split
- no random shuffle
- no future features
- point-in-time correct feature retrieval

## Run

```bash
pip install -r requirements.txt
python -m data.generate
python -m quality.validate
python -m features.build
python -m training.train
python -m monitoring.evaluate_drift
```

## Production extensions

- Feast online store
- Iceberg catalog
- OpenLineage
- MLflow model registry
- Evidently
- Terraform
- Kubernetes
- GitHub Actions
