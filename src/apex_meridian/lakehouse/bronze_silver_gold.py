from __future__ import annotations

import csv
import shutil
from collections import defaultdict
from pathlib import Path

from apex_meridian.governance.pii import mask_record
from apex_meridian.lakehouse.delta_log import write_delta_commit


def land_bronze(source_file: Path, bronze_table: Path) -> Path:
    bronze_table.mkdir(parents=True, exist_ok=True)
    target = bronze_table / source_file.name
    shutil.copyfile(source_file, target)
    write_delta_commit(bronze_table, "STREAMING_APPEND", [target.name], {"inputFiles": 1})
    return target


def transform_transactions_to_silver(bronze_file: Path, silver_table: Path) -> Path:
    silver_table.mkdir(parents=True, exist_ok=True)
    target = silver_table / f"silver_{bronze_file.name}"
    seen: set[str] = set()
    written = 0
    with bronze_file.open(newline="", encoding="utf-8") as source, target.open(
        "w", newline="", encoding="utf-8"
    ) as sink:
        reader = csv.DictReader(source)
        fieldnames = list(reader.fieldnames or []) + ["risk_band"]
        writer = csv.DictWriter(sink, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            transaction_id = row.get("transaction_id", "")
            if not transaction_id or transaction_id in seen:
                continue
            seen.add(transaction_id)
            amount = float(row.get("amount") or 0)
            risk_signals = int(row.get("risk_signal_count") or 0)
            risk_band = "high" if amount > 900 or risk_signals >= 4 else "medium" if risk_signals >= 2 else "low"
            clean_row = mask_record(row)
            clean_row["risk_band"] = risk_band
            writer.writerow(clean_row)
            written += 1
    write_delta_commit(silver_table, "MERGE_DEDUPED", [target.name], {"outputRows": written})
    return target


def build_gold_fraud_kpis(silver_file: Path, gold_table: Path) -> Path:
    gold_table.mkdir(parents=True, exist_ok=True)
    aggregates: dict[str, dict] = defaultdict(
        lambda: {"transactions": 0, "amount": 0.0, "high_risk_transactions": 0}
    )
    with silver_file.open(newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        for row in reader:
            key = row["event_ts"][:10]
            aggregates[key]["transactions"] += 1
            aggregates[key]["amount"] += float(row.get("amount") or 0)
            if row.get("risk_band") == "high":
                aggregates[key]["high_risk_transactions"] += 1

    target = gold_table / "fraud_daily_kpis.csv"
    with target.open("w", newline="", encoding="utf-8") as sink:
        fieldnames = ["business_date", "transactions", "amount", "high_risk_transactions", "risk_rate_bps"]
        writer = csv.DictWriter(sink, fieldnames=fieldnames)
        writer.writeheader()
        for business_date, values in sorted(aggregates.items()):
            risk_rate = 10_000 * values["high_risk_transactions"] / max(values["transactions"], 1)
            writer.writerow(
                {
                    "business_date": business_date,
                    "transactions": values["transactions"],
                    "amount": round(values["amount"], 2),
                    "high_risk_transactions": values["high_risk_transactions"],
                    "risk_rate_bps": round(risk_rate, 2),
                }
            )
    write_delta_commit(gold_table, "GOLD_AGGREGATE", [target.name], {"businessDates": len(aggregates)})
    return target

