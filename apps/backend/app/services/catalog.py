from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone


PLATFORM_SNAPSHOT = {
    "as_of": "2026-06-16T09:00:00Z",
    "institution": "Apex Meridian Bank",
    "platform": "Apex Meridian Bank Intelligence Platform",
    "executive_kpis": {
        "transaction_volume_7d": 128_450_982,
        "transaction_amount_7d": 18_742_550_913.42,
        "fraud_loss_avoided_7d": 24_840_150.25,
        "confirmed_fraud_rate_bps": 18.7,
        "chargeback_rate_bps": 31.4,
        "active_customers": 8_420_000,
        "high_risk_merchants": 183,
        "pipeline_sla_percent": 99.63,
        "gold_quality_score": 98.4,
        "ai_reports_validated": 42,
    },
    "fraud_metrics": {
        "weekly_trend": [
            {"day": "Mon", "alerts": 18124, "confirmed": 1921, "loss_avoided": 3_520_000},
            {"day": "Tue", "alerts": 20418, "confirmed": 2142, "loss_avoided": 3_940_000},
            {"day": "Wed", "alerts": 22672, "confirmed": 2433, "loss_avoided": 4_310_000},
            {"day": "Thu", "alerts": 21809, "confirmed": 2351, "loss_avoided": 4_020_000},
            {"day": "Fri", "alerts": 26791, "confirmed": 3128, "loss_avoided": 5_830_000},
            {"day": "Sat", "alerts": 23964, "confirmed": 2710, "loss_avoided": 4_780_000},
            {"day": "Sun", "alerts": 18731, "confirmed": 1904, "loss_avoided": 3_210_000},
        ],
        "high_risk_categories": [
            {"category": "Cross-border luxury resale", "risk_score": 94, "volume_delta_pct": 18.6},
            {"category": "Digital gaming marketplaces", "risk_score": 91, "volume_delta_pct": 22.1},
            {"category": "Expedited travel brokers", "risk_score": 88, "volume_delta_pct": 14.4},
            {"category": "Electronics repair aggregators", "risk_score": 83, "volume_delta_pct": 9.9},
        ],
        "regional_patterns": [
            {"region": "Northeast", "risk_score": 72, "chargeback_delta_pct": 4.8},
            {"region": "Southeast", "risk_score": 79, "chargeback_delta_pct": 8.2},
            {"region": "Midwest", "risk_score": 61, "chargeback_delta_pct": -1.7},
            {"region": "West", "risk_score": 84, "chargeback_delta_pct": 11.5},
        ],
    },
    "customer_360": {
        "segments": [
            {"segment": "Meridian Prime", "customers": 920_000, "avg_balance": 84_300, "risk": 21},
            {"segment": "Apex Everyday", "customers": 4_800_000, "avg_balance": 7_950, "risk": 44},
            {"segment": "Summit Credit Builder", "customers": 1_970_000, "avg_balance": 2_140, "risk": 63},
            {"segment": "Horizon Small Business", "customers": 730_000, "avg_balance": 31_600, "risk": 38},
        ],
        "behavior_changes": [
            {"metric": "mobile_wallet_spend", "change_pct": 12.8},
            {"metric": "cash_advance_frequency", "change_pct": 3.4},
            {"metric": "loan_autopay_adoption", "change_pct": 5.9},
            {"metric": "reward_redemption_value", "change_pct": 8.1},
        ],
    },
    "data_quality": {
        "scorecards": [
            {"dataset": "gold.fraud_daily_kpis", "score": 99.1, "failed_rules": 0, "freshness_minutes": 11},
            {"dataset": "gold.customer_360", "score": 98.8, "failed_rules": 1, "freshness_minutes": 22},
            {"dataset": "silver.card_transactions", "score": 97.4, "failed_rules": 3, "freshness_minutes": 7},
            {"dataset": "silver.loan_payments", "score": 98.2, "failed_rules": 1, "freshness_minutes": 18},
            {"dataset": "bronze.fraud_alerts_raw", "score": 96.7, "failed_rules": 2, "freshness_minutes": 3},
        ]
    },
    "pipeline_status": {
        "jobs": [
            {"name": "daily_batch_ingestion", "status": "healthy", "sla": "met", "duration_min": 18},
            {"name": "stream_checkpoint_validation", "status": "healthy", "sla": "met", "duration_min": 4},
            {"name": "bronze_to_silver_transform", "status": "healthy", "sla": "met", "duration_min": 31},
            {"name": "silver_to_gold_kpi_publish", "status": "healthy", "sla": "met", "duration_min": 12},
            {"name": "fraud_model_scoring", "status": "watch", "sla": "met", "duration_min": 16},
            {"name": "ai_report_validation", "status": "healthy", "sla": "met", "duration_min": 6},
        ],
        "lakehouse_layers": [
            {"layer": "Bronze", "records_7d": 142_900_441, "partitions": 168, "retention_days": 730},
            {"layer": "Silver", "records_7d": 139_730_205, "partitions": 168, "retention_days": 365},
            {"layer": "Gold", "records_7d": 18_420_991, "partitions": 84, "retention_days": 2555},
        ],
    },
    "lineage": {
        "nodes": [
            "mysql.core_customers",
            "postgres.card_authorizations",
            "mongo.digital_sessions",
            "cassandra.payment_events",
            "kafka.card.transactions.raw",
            "bronze.transactions_raw",
            "silver.card_transactions",
            "gold.fraud_daily_kpis",
            "gold.customer_360",
            "warehouse.executive_risk_mart",
            "vector.governed_metric_context",
            "ai.weekly_risk_report",
        ],
        "edges": [
            ["postgres.card_authorizations", "kafka.card.transactions.raw"],
            ["kafka.card.transactions.raw", "bronze.transactions_raw"],
            ["bronze.transactions_raw", "silver.card_transactions"],
            ["silver.card_transactions", "gold.fraud_daily_kpis"],
            ["silver.card_transactions", "gold.customer_360"],
            ["gold.fraud_daily_kpis", "warehouse.executive_risk_mart"],
            ["warehouse.executive_risk_mart", "vector.governed_metric_context"],
            ["vector.governed_metric_context", "ai.weekly_risk_report"],
        ],
    },
    "governance": {
        "policies": [
            {"id": "PII-001", "name": "Customer direct identifier masking", "status": "active"},
            {"id": "RBAC-004", "name": "Gold-layer executive metrics access", "status": "active"},
            {"id": "AI-007", "name": "Cited-answer enforcement for AI reporting", "status": "active"},
            {"id": "RET-009", "name": "Seven-year regulatory KPI retention", "status": "active"},
        ]
    },
    "audit_logs": [
        {
            "event_id": "audit-20260616-0001",
            "actor": "airflow:fraud_model_scoring",
            "action": "score_transactions",
            "dataset": "silver.card_transactions",
            "status": "success",
            "timestamp": "2026-06-16T08:41:18Z",
        },
        {
            "event_id": "audit-20260616-0002",
            "actor": "ai-agent:weekly_report",
            "action": "validate_report_metrics",
            "dataset": "gold.fraud_daily_kpis",
            "status": "success",
            "timestamp": "2026-06-16T08:55:04Z",
        },
    ],
}


def snapshot() -> dict:
    live_snapshot = deepcopy(PLATFORM_SNAPSHOT)
    live_snapshot["served_at"] = datetime.now(timezone.utc).isoformat()
    return live_snapshot

