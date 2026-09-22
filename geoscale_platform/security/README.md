# Security checklist

Before production:

- never put credentials in Git
- use IAM roles / workload identity
- use Secrets Manager / Kubernetes Secrets
- encrypt S3/object storage
- TLS for Kafka/API
- private subnets for data services
- network policies in Kubernetes
- dependency scanning
- container image scanning
- signed artifacts
- least privilege IAM
- audit logs
- rate limiting
- request validation
- PII classification if real data is introduced
