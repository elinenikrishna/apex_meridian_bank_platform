from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class FraudScore:
    transaction_id: str
    score: float
    risk_band: str
    reason_codes: list[str]


class FraudAnomalyScorer:
    """Deterministic fallback scorer mirroring features used by the Spark production job."""

    def score(self, transaction: dict) -> FraudScore:
        amount = float(transaction.get("amount") or 0)
        device_trust = float(transaction.get("device_trust_score") or 0.5)
        risk_signals = int(transaction.get("risk_signal_count") or 0)
        card_present = str(transaction.get("card_present")).lower() == "true"
        category = str(transaction.get("merchant_category") or "")

        score = 0.18
        score += min(math.log1p(amount) / 12, 0.28)
        score += risk_signals * 0.09
        score += (1 - device_trust) * 0.22
        if not card_present:
            score += 0.08
        if category in {"Cross-border luxury resale", "Digital gaming marketplaces"}:
            score += 0.12

        score = round(min(score, 0.99), 4)
        risk_band = "critical" if score >= 0.82 else "high" if score >= 0.66 else "medium" if score >= 0.42 else "low"
        reasons = []
        if amount > 900:
            reasons.append("AMOUNT_SPIKE")
        if risk_signals >= 3:
            reasons.append("MULTIPLE_RISK_SIGNALS")
        if device_trust < 0.35:
            reasons.append("LOW_DEVICE_TRUST")
        if not card_present:
            reasons.append("CARD_NOT_PRESENT")
        if category in {"Cross-border luxury resale", "Digital gaming marketplaces"}:
            reasons.append("HIGH_RISK_MERCHANT_CATEGORY")
        return FraudScore(
            transaction_id=str(transaction.get("transaction_id", "")),
            score=score,
            risk_band=risk_band,
            reason_codes=reasons or ["BASELINE_BEHAVIOR"],
        )

