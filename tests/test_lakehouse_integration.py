import csv
from pathlib import Path

from apex_meridian.lakehouse.bronze_silver_gold import (
    build_gold_fraud_kpis,
    land_bronze,
    transform_transactions_to_silver,
)


def test_local_bronze_silver_gold_flow(tmp_path: Path):
    source = tmp_path / "source.csv"
    with source.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "transaction_id",
                "customer_id",
                "account_id",
                "merchant_id",
                "event_ts",
                "amount",
                "currency",
                "merchant_category",
                "channel",
                "region",
                "authorization_status",
                "device_trust_score",
                "card_present",
                "risk_signal_count",
            ],
        )
        writer.writeheader()
        writer.writerow(
            {
                "transaction_id": "TXN-1",
                "customer_id": "CUST-1",
                "account_id": "ACCT-1",
                "merchant_id": "MERC-1",
                "event_ts": "2026-01-01T00:00:00Z",
                "amount": "1200",
                "currency": "USD",
                "merchant_category": "Cross-border luxury resale",
                "channel": "ecommerce",
                "region": "West",
                "authorization_status": "approved",
                "device_trust_score": "0.24",
                "card_present": "False",
                "risk_signal_count": "5",
            }
        )

    bronze = land_bronze(source, tmp_path / "bronze")
    silver = transform_transactions_to_silver(bronze, tmp_path / "silver")
    gold = build_gold_fraud_kpis(silver, tmp_path / "gold")

    assert bronze.exists()
    assert silver.exists()
    assert gold.exists()
    assert (tmp_path / "gold" / "_delta_log" / "00000000000000000000.json").exists()

