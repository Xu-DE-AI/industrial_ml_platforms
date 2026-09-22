# Production readiness checklist

Use this after both projects.

## Data
- [ ] schema versioning
- [ ] data contracts
- [ ] quality gates
- [ ] duplicate handling
- [ ] late-arriving data
- [ ] backfills
- [ ] partition strategy
- [ ] compaction
- [ ] retention

## ML
- [ ] baseline
- [ ] time-based validation
- [ ] leakage tests
- [ ] class imbalance strategy
- [ ] calibration
- [ ] experiment tracking
- [ ] model registry
- [ ] reproducible training
- [ ] model signature

## Features
- [ ] offline/online consistency
- [ ] point-in-time correctness
- [ ] feature versioning
- [ ] feature freshness

## Serving
- [ ] health
- [ ] readiness
- [ ] timeout
- [ ] retries
- [ ] rate limiting
- [ ] p50/p95/p99
- [ ] autoscaling
- [ ] graceful shutdown

## Distributed systems
- [ ] partitioning
- [ ] skew handling
- [ ] broadcast joins
- [ ] backpressure
- [ ] checkpointing
- [ ] idempotency
- [ ] dead-letter queue

## Operations
- [ ] structured logs
- [ ] metrics
- [ ] traces
- [ ] alerts
- [ ] drift
- [ ] rollback
- [ ] canary
- [ ] disaster recovery

## Security
- [ ] secrets outside Git
- [ ] IAM
- [ ] encryption
- [ ] network policies
- [ ] dependency scanning
- [ ] image scanning

## Infrastructure
- [ ] Terraform
- [ ] Kubernetes
- [ ] CI/CD
- [ ] environment separation
- [ ] cost monitoring
