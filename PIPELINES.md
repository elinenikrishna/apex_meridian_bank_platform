# Pipelines

## Daily Batch Ingestion

Generates or ingests customers, merchants, transactions, loan payments, rewards, fraud alerts, and chargebacks. In production this pattern maps to file drops, JDBC extracts, and CDC snapshots.

## Streaming Ingestion

Kafka topics are defined in [pipelines/kafka/topics.yaml](pipelines/kafka/topics.yaml). The Spark stream lands raw payloads to Bronze with checkpoints for exactly-once processing semantics.

## Bronze to Silver

Silver transformations perform:

- Schema validation
- Null handling
- Deduplication by business key
- PII masking and tokenization
- Risk band enrichment
- Partitioning by event date
- Data quality measurement

## Silver to Gold

Gold transformations publish:

- Fraud daily KPIs
- Customer 360 aggregates
- Merchant category risk KPIs
- Chargeback spike metrics
- Pipeline SLA and freshness scorecards
- Regulatory weekly reporting tables

## Warehouse Loading

SQL models under [pipelines/sql/marts](pipelines/sql/marts) represent Snowflake-style, BigQuery-style, and Redshift-style analytics layers.

## AI Context Preparation

Approved Gold metrics and catalog metadata are indexed into the vector context layer. Non-Gold datasets are excluded from chatbot answers by default.

## PDF Report Generation

[scripts/generate_weekly_report.py](scripts/generate_weekly_report.py) creates a weekly executive risk report under `outputs/` and validates narrative metrics against Gold KPI values.

