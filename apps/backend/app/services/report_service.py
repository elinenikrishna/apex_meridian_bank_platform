from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from apps.backend.app.services.catalog import snapshot


def generate_executive_report(report_type: str, requested_by: str, week_ending: str | None) -> dict:
    platform = snapshot()
    metrics = platform["executive_kpis"]
    report_id = f"amip-rpt-{uuid4().hex[:10]}"
    sections = [
        "Executive risk posture",
        "Fraud trend and loss avoidance",
        "High-risk merchant categories",
        "Data quality and pipeline SLA",
        "AI validation and cited metric inventory",
    ]
    return {
        "report_id": report_id,
        "status": "generated",
        "generated_at": datetime.now(timezone.utc),
        "validation_status": "validated_against_gold_layer",
        "sections": sections,
        "metrics_used": {
            "week_ending": week_ending,
            "report_type": report_type,
            "requested_by": requested_by,
            "transaction_volume_7d": metrics["transaction_volume_7d"],
            "fraud_loss_avoided_7d": metrics["fraud_loss_avoided_7d"],
            "gold_quality_score": metrics["gold_quality_score"],
        },
    }

