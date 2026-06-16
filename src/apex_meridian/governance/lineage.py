from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LineageEdge:
    source: str
    target: str
    transformation: str


ENTERPRISE_LINEAGE = [
    LineageEdge("mysql.customer_master", "bronze.customer_profiles_raw", "daily CDC ingest"),
    LineageEdge("postgres.card_authorizations", "kafka.card.transactions.raw", "outbox event stream"),
    LineageEdge("kafka.card.transactions.raw", "bronze.card_transactions_raw", "stream landing"),
    LineageEdge("bronze.card_transactions_raw", "silver.card_transactions", "schema validation, dedupe, PII policy"),
    LineageEdge("silver.card_transactions", "gold.fraud_daily_kpis", "risk feature aggregation"),
    LineageEdge("silver.card_transactions", "gold.customer_360", "customer behavior rollup"),
    LineageEdge("gold.fraud_daily_kpis", "warehouse.executive_risk_mart", "warehouse sync"),
    LineageEdge("warehouse.executive_risk_mart", "vector.governed_metric_context", "approved context indexing"),
    LineageEdge("vector.governed_metric_context", "ai.weekly_risk_report", "cited AI generation"),
]


def lineage_graph() -> dict:
    nodes = sorted({edge.source for edge in ENTERPRISE_LINEAGE} | {edge.target for edge in ENTERPRISE_LINEAGE})
    return {
        "nodes": nodes,
        "edges": [
            {"source": edge.source, "target": edge.target, "transformation": edge.transformation}
            for edge in ENTERPRISE_LINEAGE
        ],
    }

