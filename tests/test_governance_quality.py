import csv

from apex_meridian.governance.quality import evaluate_csv


def test_quality_score_detects_negative_amount(tmp_path):
    path = tmp_path / "transactions.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["transaction_id", "customer_id", "amount", "event_ts"])
        writer.writeheader()
        writer.writerow({"transaction_id": "T1", "customer_id": "C1", "amount": "12.40", "event_ts": "2026-01-01"})
        writer.writerow({"transaction_id": "T2", "customer_id": "C2", "amount": "-1", "event_ts": "2026-01-01"})

    result = evaluate_csv(path)
    assert result["failed_checks"] == 1
    assert result["score"] < 100

