## Architecture

```text
Sensors
  |
  v
Kafka / Redpanda
  |
  +------------------------+
  |                        |
  v                        v
Flink streaming       S3 / object storage
  |                        |
  v                        v
online features         Iceberg
  |                        |
  |                     Spark
  |                        |
  +-----------+------------+
              |
          ML features
              |
       +------+------+
       |             |
     MLflow        DDP/FSDP
       |             |
       +------+------+
              |
         Model Registry
              |
          FastAPI
              |
        Kubernetes
              |
      Prometheus/Grafana
```

## Local startup

```bash
pip install -r requirements.txt
python -m data.generate
python -m data.validate
docker compose -f infra/docker-compose.yml up -d
```

Then:

```bash
python -m training.train
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Important labs

### Lakehouse
`lakehouse/iceberg_lab.py`

Demonstrates:

- partitioned Parquet/Iceberg layout
- schema evolution
- MERGE/upsert concepts
- snapshots/time-travel concepts
- compaction

### Data quality
`quality/schema.py`

Pandera checks:

- types
- nullability
- physical ranges
- temporal ordering
- duplicate event IDs

### Streaming
`streaming/producer.py`

Publishes sensor events with a stable key.

`streaming/consumer.py`

Uses manual commits and an idempotency store.

### ML
`training/train.py`

- time split
- baseline logistic regression
- XGBoost
- MLflow logging
- model signature
- calibration metrics

`training/ddp_train.py`

Educational DDP implementation.

### Serving
`app/main.py`

FastAPI:

- `/health`
- `/ready`
- `/predict`
- `/metrics`

### Operations
- Prometheus metrics
- Grafana dashboard
- Docker health checks
- Kubernetes deployment
- Terraform AWS skeleton
- GitHub Actions
- security checklist
- load test


