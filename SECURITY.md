# Security

## Data Classification

- Bronze: restricted raw data, no direct AI use.
- Silver: confidential trusted data, PII masked or tokenized.
- Gold: governed business-ready metrics, approved for executive dashboards and AI context.

## PII Masking

[src/apex_meridian/governance/pii.py](src/apex_meridian/governance/pii.py) masks email and phone values and tokenizes direct identifiers such as full name and SSN token.

## RBAC

RBAC policies define which roles can access which datasets. The chatbot and report generator are designed to enforce Gold-only access for executive analytics.

## Audit Logging

Audit events capture actor, action, dataset, status, timestamp, and metadata. AI answers include audit identifiers for downstream compliance review.

## Secrets

`.env.example` documents required variables. Real deployments should use Kubernetes secrets, cloud secret managers, or CI/CD secret stores instead of plaintext files.

## Network Controls

Production deployments should isolate Kafka, databases, object storage, Airflow, and API services into private subnets with service-to-service identity and mTLS where available.

