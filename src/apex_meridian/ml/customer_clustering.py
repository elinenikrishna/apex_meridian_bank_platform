from __future__ import annotations


def assign_behavior_cluster(profile: dict) -> dict:
    avg_balance = float(profile.get("avg_balance", 0))
    risk_score = float(profile.get("risk_score", 50))
    transaction_count = int(profile.get("transaction_count_90d", 0))

    if avg_balance > 50_000 and risk_score < 35:
        cluster = "relationship_growth"
    elif risk_score > 70:
        cluster = "risk_intervention"
    elif transaction_count > 140:
        cluster = "digital_power_user"
    else:
        cluster = "core_banking"

    return {
        "customer_id": profile.get("customer_id"),
        "behavior_cluster": cluster,
        "features": {
            "avg_balance": avg_balance,
            "risk_score": risk_score,
            "transaction_count_90d": transaction_count,
        },
    }

