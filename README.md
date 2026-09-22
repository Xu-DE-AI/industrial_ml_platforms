
## Common engineering principles

- data contracts before modeling
- idempotent ingestion
- partitioned columnar storage
- schema evolution
- data quality gates
- lineage
- reproducible training
- experiment tracking
- model registry
- offline/online feature consistency
- time-based validation
- calibration
- drift monitoring
- API health/readiness
- structured logging
- metrics
- retries and dead-letter paths
- CI/CD
- infrastructure as code
- least-privilege security
- load testing
- rollback/canary concepts

## Recommended order

### Project A
```text
GeoScale
  1. data contract
  2. Parquet/Iceberg
  3. Pandera
  4. Spark
  5. Kafka
  6. Flink
  7. MLflow
  8. DDP
  9. FastAPI
 10. Prometheus/Grafana
 11. Terraform
 12. Kubernetes
 13. CI/CD
```

### Project B
```text
Geothermal Intelligence
  1. lakehouse
  2. quality
  3. feature engineering
  4. Feast
  5. XGBoost
  6. calibration
  7. MLflow registry
  8. drift monitoring
  9. OpenLineage
 10. API
 11. Kubernetes
 12. Terraform
```


