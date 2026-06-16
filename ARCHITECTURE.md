# Architecture

## Overview

Apex Meridian Bank Intelligence Platform is organized as a multi-layer enterprise data architecture. The system separates raw ingestion, trusted transformation, governed analytics, AI context, and executive delivery.

## Logical Components

- **Source Systems:** PostgreSQL card authorization events, MySQL customer core, MongoDB digital sessions, Cassandra payment events, and file-based regulatory extracts.
- **Event Streaming:** Kafka topics capture card transactions, merchant events, customer profile updates, fraud alerts, payment events, rewards events, AI report requests, and audit events.
- **Batch and CDC Ingestion:** Airflow schedules file, database, and CDC-style ingestion into raw landing paths.
- **Bronze Layer:** Immutable raw data with event payloads, source timestamps, ingestion metadata, and replay support.
- **Silver Layer:** Schema validated, deduplicated, masked, enriched, and conformed records.
- **Gold Layer:** Business-ready KPIs, Customer 360 aggregates, fraud risk marts, data quality scorecards, and regulatory reporting tables.
- **Warehouse Layer:** Snowflake-style, BigQuery-style, and Redshift-style marts represented by SQL models and API contracts.
- **Vector Context Layer:** Approved Gold metadata and KPI facts indexed for RAG.
- **AI Governance Layer:** Prompt versioning, source citation, hallucination checks, refusal logic, and answer audit.
- **Dashboard Layer:** Premium executive app and FastAPI services.
- **Monitoring and Audit:** Pipeline status, quality scorecards, lineage graph, and immutable audit events.

## Storage Compatibility

Local paths use `data/lakehouse`, but the project documents equivalent storage roots:

- S3: `s3://apex-meridian-lakehouse/bronze|silver|gold`
- Azure Data Lake: `abfss://apex-meridian@.../bronze|silver|gold`
- Google Cloud Storage: `gs://apex-meridian-lakehouse/bronze|silver|gold`

## Partition Strategy

- Transactions: `event_date`, `region`
- Fraud alerts: `event_date`, `alert_type`
- Loan payments: `event_date`, `days_past_due_bucket`
- Customer profiles: `snapshot_date`, `home_region`
- Gold KPIs: `business_date`

## Schema Evolution

Bronze is append-only and tolerant of new raw fields. Silver jobs use explicit schema validation and controlled `mergeSchema` for additive fields. Gold tables require documented contract changes and downstream dashboard validation.

## Time Travel

Delta-style commit logs in `_delta_log` document append and merge operations. Production Delta Lake can query previous versions for reconciliation, regulatory investigations, and report restatement review.

