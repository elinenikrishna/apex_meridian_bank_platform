from __future__ import annotations

from uuid import uuid4

from apex_meridian.rag.vector_index import SimpleTfidfVectorIndex

SUPPORTED_TOPICS = {
    "fraud": "gold.fraud_daily_kpis",
    "merchant": "gold.merchant_risk_kpis",
    "transaction": "gold.transaction_volume_kpis",
    "customer": "gold.customer_360",
    "chargeback": "gold.chargeback_kpis",
    "regional": "gold.regional_risk_kpis",
    "quality": "gold.data_quality_scorecards",
    "pipeline": "gold.pipeline_observability",
    "kpi": "warehouse.executive_risk_mart",
}


class GovernedBankingChatbot:
    def __init__(self, index: SimpleTfidfVectorIndex, snapshot: dict):
        self.index = index
        self.snapshot = snapshot

    @classmethod
    def from_platform_snapshot(cls, snapshot: dict) -> "GovernedBankingChatbot":
        index = SimpleTfidfVectorIndex()
        kpis = snapshot["executive_kpis"]
        index.add(
            "gold.fraud_daily_kpis",
            (
                f"Fraud trend: confirmed fraud rate is {kpis['confirmed_fraud_rate_bps']} bps, "
                f"loss avoided is ${kpis['fraud_loss_avoided_7d']:,.2f}, "
                f"and high-risk merchants total {kpis['high_risk_merchants']}."
            ),
            {"dataset": "gold.fraud_daily_kpis", "layer": "Gold"},
        )
        index.add(
            "gold.transaction_volume_kpis",
            (
                f"Transaction volume for the last seven days is {kpis['transaction_volume_7d']:,}; "
                f"authorized amount is ${kpis['transaction_amount_7d']:,.2f}."
            ),
            {"dataset": "gold.transaction_volume_kpis", "layer": "Gold"},
        )
        index.add(
            "gold.data_quality_scorecards",
            f"Gold quality score is {kpis['gold_quality_score']} and pipeline SLA is {kpis['pipeline_sla_percent']}%.",
            {"dataset": "gold.data_quality_scorecards", "layer": "Gold"},
        )
        for category in snapshot["fraud_metrics"]["high_risk_categories"]:
            index.add(
                f"gold.merchant_risk_kpis::{category['category']}",
                (
                    f"Merchant category {category['category']} has risk score {category['risk_score']} "
                    f"and volume delta {category['volume_delta_pct']}%."
                ),
                {"dataset": "gold.merchant_risk_kpis", "layer": "Gold"},
            )
        return cls(index=index, snapshot=snapshot)

    def answer(self, question: str, role: str = "risk_executive", user_id: str = "demo") -> dict:
        normalized = question.lower()
        matched_dataset = None
        for keyword, dataset in SUPPORTED_TOPICS.items():
            if keyword in normalized:
                matched_dataset = dataset
                break

        audit_event_id = f"ai-audit-{uuid4().hex[:12]}"
        if matched_dataset is None:
            return {
                "answer": (
                    "I can only answer from governed Gold Layer metrics and approved metadata. "
                    "This question requires an approved dataset that is not indexed yet."
                ),
                "confidence": 0.0,
                "refused": True,
                "citations": [],
                "audit_event_id": audit_event_id,
            }

        results = self.index.search(question, limit=3)
        if not results:
            return {
                "answer": (
                    f"The topic is governed, but no approved context was found for {matched_dataset}. "
                    f"Index {matched_dataset} into the vector context layer before answering."
                ),
                "confidence": 0.1,
                "refused": True,
                "citations": [matched_dataset],
                "audit_event_id": audit_event_id,
            }

        facts = " ".join(result["text"] for result in results)
        citations = sorted({result["metadata"].get("dataset", result["doc_id"]) for result in results})
        return {
            "answer": f"Based on governed Gold Layer context: {facts}",
            "confidence": min(0.96, 0.72 + 0.08 * len(results)),
            "refused": False,
            "citations": citations,
            "audit_event_id": audit_event_id,
        }

