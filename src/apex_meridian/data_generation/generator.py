from __future__ import annotations

import argparse
import csv
import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Callable, Iterable

from apex_meridian.data_generation.schemas import DOMAIN_COLUMNS

FIRST_NAMES = [
    "Ari",
    "Maya",
    "Nolan",
    "Priya",
    "Sofia",
    "Elias",
    "Lina",
    "Marcus",
    "Iris",
    "Dev",
]
LAST_NAMES = [
    "Vale",
    "Reyes",
    "Iyer",
    "Stone",
    "Morgan",
    "Kline",
    "Shah",
    "Rowan",
    "Chen",
    "Okafor",
]
REGIONS = ["Northeast", "Southeast", "Midwest", "West", "Southwest", "Pacific"]
MERCHANT_CATEGORIES = [
    "Everyday grocery",
    "Fuel and mobility",
    "Digital gaming marketplaces",
    "Healthcare services",
    "Cross-border luxury resale",
    "Expedited travel brokers",
    "Electronics repair aggregators",
    "Restaurants",
]
CHANNELS = ["chip", "tap", "ecommerce", "mobile_wallet", "atm", "recurring"]
SEGMENTS = ["Meridian Prime", "Apex Everyday", "Summit Credit Builder", "Horizon Small Business"]


def _event_time(index: int) -> str:
    base = datetime(2026, 1, 1, tzinfo=timezone.utc)
    return (base + timedelta(seconds=index * 17)).isoformat()


def _customer_id(index: int) -> str:
    return f"CUST-{index % 8_500_000:010d}"


def _merchant_id(index: int) -> str:
    return f"MERC-{index % 125_000:08d}"


def customer_record(index: int, rng: random.Random) -> dict:
    first = rng.choice(FIRST_NAMES)
    last = rng.choice(LAST_NAMES)
    return {
        "customer_id": _customer_id(index),
        "full_name": f"{first} {last}",
        "email": f"{first.lower()}.{last.lower()}{index % 9973}@example.apex",
        "phone": f"+1-555-{index % 900 + 100:03d}-{index % 10000:04d}",
        "ssn_token": f"tok_ssn_{index:012d}",
        "segment": rng.choice(SEGMENTS),
        "home_region": rng.choice(REGIONS),
        "opened_date": (datetime(2014, 1, 1) + timedelta(days=index % 4100)).date().isoformat(),
        "kyc_status": rng.choices(["verified", "review", "restricted"], weights=[94, 5, 1])[0],
        "annual_income_band": rng.choice(["0-50k", "50-100k", "100-250k", "250k+"]),
    }


def merchant_record(index: int, rng: random.Random) -> dict:
    category = MERCHANT_CATEGORIES[index % len(MERCHANT_CATEGORIES)]
    return {
        "merchant_id": _merchant_id(index),
        "merchant_name": f"Astra {category.split()[0]} Market {index % 50_000}",
        "merchant_category": category,
        "region": rng.choice(REGIONS),
        "onboarding_risk_tier": rng.choices(["low", "medium", "high"], weights=[76, 19, 5])[0],
        "active_since": (datetime(2016, 1, 1) + timedelta(days=index % 3200)).date().isoformat(),
    }


def transaction_record(index: int, rng: random.Random) -> dict:
    category = rng.choice(MERCHANT_CATEGORIES)
    amount = round(max(1.0, rng.lognormvariate(3.55, 1.05)), 2)
    risky_category = category in {"Cross-border luxury resale", "Digital gaming marketplaces"}
    risk_signal_count = rng.randint(0, 2) + (rng.randint(2, 5) if risky_category and rng.random() < 0.08 else 0)
    return {
        "transaction_id": f"TXN-{index:016d}",
        "customer_id": _customer_id(index + rng.randint(0, 90_000)),
        "account_id": f"ACCT-{index % 9_200_000:010d}",
        "merchant_id": _merchant_id(index + rng.randint(0, 10_000)),
        "event_ts": _event_time(index),
        "amount": amount,
        "currency": "USD",
        "merchant_category": category,
        "channel": rng.choice(CHANNELS),
        "region": rng.choice(REGIONS),
        "authorization_status": rng.choices(["approved", "declined", "review"], [93, 5, 2])[0],
        "device_trust_score": round(rng.uniform(0.12, 0.99), 3),
        "card_present": rng.choice([True, False]),
        "risk_signal_count": risk_signal_count,
    }


def loan_payment_record(index: int, rng: random.Random) -> dict:
    amount = round(rng.uniform(125, 3200), 2)
    principal = round(amount * rng.uniform(0.55, 0.93), 2)
    return {
        "payment_id": f"LPAY-{index:014d}",
        "loan_id": f"LOAN-{index % 1_800_000:010d}",
        "customer_id": _customer_id(index),
        "event_ts": _event_time(index),
        "amount": amount,
        "principal_component": principal,
        "interest_component": round(amount - principal, 2),
        "days_past_due": rng.choices([0, 1, 5, 15, 30, 60, 90], [82, 5, 4, 3, 3, 2, 1])[0],
        "payment_channel": rng.choice(["autopay", "branch", "mobile", "web", "lockbox"]),
    }


def rewards_record(index: int, rng: random.Random) -> dict:
    redeemed = rng.choice([0, 0, 0, rng.randint(100, 20000)])
    return {
        "reward_event_id": f"RWD-{index:014d}",
        "customer_id": _customer_id(index),
        "transaction_id": f"TXN-{index:016d}",
        "event_ts": _event_time(index),
        "points_earned": rng.randint(1, 750),
        "points_redeemed": redeemed,
        "reward_program": rng.choice(["Meridian Miles", "Apex Cash", "Summit Secure Rewards"]),
    }


def fraud_alert_record(index: int, rng: random.Random) -> dict:
    alert_type = rng.choice(["velocity", "merchant_risk", "device_mismatch", "geo_impossible", "amount_spike"])
    return {
        "alert_id": f"ALERT-{index:014d}",
        "transaction_id": f"TXN-{index:016d}",
        "customer_id": _customer_id(index),
        "event_ts": _event_time(index),
        "alert_type": alert_type,
        "alert_score": round(rng.uniform(0.52, 0.99), 4),
        "case_status": rng.choices(["open", "cleared", "confirmed", "escalated"], [18, 61, 17, 4])[0],
        "analyst_queue": rng.choice(["card-risk-east", "card-risk-west", "digital-risk", "merchant-risk"]),
    }


def chargeback_record(index: int, rng: random.Random) -> dict:
    return {
        "chargeback_id": f"CBK-{index:014d}",
        "transaction_id": f"TXN-{index:016d}",
        "customer_id": _customer_id(index),
        "merchant_id": _merchant_id(index),
        "event_ts": _event_time(index),
        "dispute_reason": rng.choice(["not_recognized", "duplicate", "service_not_received", "fraud_claim"]),
        "amount": round(rng.uniform(12, 2200), 2),
        "status": rng.choices(["opened", "won", "lost", "provisional_credit"], [20, 42, 18, 20])[0],
    }


def account_balance_record(index: int, rng: random.Random) -> dict:
    ledger = round(rng.lognormvariate(8.25, 1.15), 2)
    hold = round(rng.uniform(0, min(ledger, 5000)), 2)
    return {
        "balance_id": f"BAL-{index:014d}",
        "account_id": f"ACCT-{index % 9_200_000:010d}",
        "customer_id": _customer_id(index),
        "snapshot_date": (datetime(2026, 1, 1) + timedelta(days=index % 180)).date().isoformat(),
        "ledger_balance": ledger,
        "available_balance": round(ledger - hold, 2),
        "currency": "USD",
        "account_type": rng.choice(["checking", "savings", "credit_card", "loan"]),
        "region": rng.choice(REGIONS),
    }


def risk_score_record(index: int, rng: random.Random) -> dict:
    fraud = rng.randint(1, 99)
    aml = max(1, min(99, fraud + rng.randint(-18, 22)))
    credit = rng.randint(300, 850)
    reasons = ["velocity", "balance_trend", "merchant_mix", "payment_history"]
    return {
        "risk_score_id": f"RSK-{index:014d}",
        "customer_id": _customer_id(index),
        "snapshot_date": (datetime(2026, 1, 1) + timedelta(days=index % 180)).date().isoformat(),
        "credit_risk_score": credit,
        "fraud_risk_score": fraud,
        "aml_risk_score": aml,
        "model_version": "risk-fabric-2026.2",
        "reason_codes": "|".join(rng.sample(reasons, k=2)),
    }


def regulatory_report_record(index: int, rng: random.Random) -> dict:
    report_type = rng.choice(["weekly_fraud_posture", "chargeback_monitoring", "customer_risk_summary"])
    metric_name = rng.choice(["transaction_volume", "confirmed_fraud_rate_bps", "chargeback_rate_bps", "quality_score"])
    return {
        "report_id": f"REG-{index:014d}",
        "business_date": (datetime(2026, 1, 1) + timedelta(days=index % 180)).date().isoformat(),
        "report_type": report_type,
        "metric_name": metric_name,
        "metric_value": round(rng.uniform(1, 1000000), 4),
        "source_dataset": rng.choice(["gold.fraud_daily_kpis", "gold.customer_360", "warehouse.executive_risk_mart"]),
        "control_status": rng.choices(["passed", "review", "failed"], [94, 5, 1])[0],
    }


RECORD_FACTORIES: dict[str, Callable[[int, random.Random], dict]] = {
    "transactions": transaction_record,
    "customers": customer_record,
    "merchants": merchant_record,
    "loan_payments": loan_payment_record,
    "rewards": rewards_record,
    "fraud_alerts": fraud_alert_record,
    "chargebacks": chargeback_record,
    "account_balances": account_balance_record,
    "risk_scores": risk_score_record,
    "regulatory_reports": regulatory_report_record,
}


def batched_records(domain: str, records: int, seed: int, start_index: int = 0) -> Iterable[dict]:
    rng = random.Random(seed)
    factory = RECORD_FACTORIES[domain]
    for offset in range(records):
        yield factory(start_index + offset, rng)


def write_domain_csv(
    domain: str,
    output_dir: Path,
    records: int,
    batch_size: int,
    seed: int = 4221,
) -> list[Path]:
    if domain not in DOMAIN_COLUMNS:
        raise ValueError(f"Unknown domain '{domain}'. Expected one of {sorted(DOMAIN_COLUMNS)}")

    output_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    remaining = records
    batch_id = 0
    start_index = 0
    while remaining > 0:
        current = min(batch_size, remaining)
        path = output_dir / domain / f"part-{batch_id:05d}.csv"
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=DOMAIN_COLUMNS[domain])
            writer.writeheader()
            writer.writerows(batched_records(domain, current, seed + batch_id, start_index))
        paths.append(path)
        remaining -= current
        start_index += current
        batch_id += 1
    return paths


def write_manifest(output_dir: Path, generated: dict[str, list[Path]], records: int, batch_size: int) -> Path:
    manifest = {
        "platform": "Apex Meridian Bank Intelligence Platform",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "records_per_domain": records,
        "batch_size": batch_size,
        "scale_examples": {"1M": 1_000_000, "10M": 10_000_000, "100M": 100_000_000, "500M+": 500_000_000},
        "domains": {domain: [str(path) for path in paths] for domain, paths in generated.items()},
    }
    path = output_dir / "_generation_manifest.json"
    with path.open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)
    return path


def parse_domains(value: str) -> list[str]:
    if value == "all":
        return list(DOMAIN_COLUMNS)
    return [domain.strip() for domain in value.split(",") if domain.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate scalable synthetic Apex Meridian banking data.")
    parser.add_argument("--records", type=int, default=10_000, help="Records per selected domain.")
    parser.add_argument("--batch-size", type=int, default=100_000, help="CSV rows per output file.")
    parser.add_argument("--domains", default="all", help="Comma-separated domains or 'all'.")
    parser.add_argument("--output", type=Path, default=Path("data/generated/local_demo"))
    parser.add_argument("--seed", type=int, default=4221)
    args = parser.parse_args()

    generated: dict[str, list[Path]] = {}
    for domain in parse_domains(args.domains):
        generated[domain] = write_domain_csv(domain, args.output, args.records, args.batch_size, args.seed)
    manifest = write_manifest(args.output, generated, args.records, args.batch_size)
    print(f"Generated {len(generated)} domains. Manifest: {manifest}")


if __name__ == "__main__":
    main()
