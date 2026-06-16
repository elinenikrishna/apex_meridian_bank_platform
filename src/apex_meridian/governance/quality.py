from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


@dataclass(frozen=True)
class QualityRule:
    name: str
    column: str
    predicate: Callable[[str], bool]
    severity: str = "high"


def not_null(value: str) -> bool:
    return value not in {"", "null", "None", None}


def positive_number(value: str) -> bool:
    try:
        return float(value) >= 0
    except (TypeError, ValueError):
        return False


DEFAULT_RULES = [
    QualityRule("transaction_id_present", "transaction_id", not_null),
    QualityRule("customer_id_present", "customer_id", not_null),
    QualityRule("amount_non_negative", "amount", positive_number),
    QualityRule("event_ts_present", "event_ts", not_null),
]


def evaluate_csv(path: Path, rules: list[QualityRule] | None = None, limit: int | None = None) -> dict:
    active_rules = rules or DEFAULT_RULES
    failures = {rule.name: 0 for rule in active_rules}
    rows = 0
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows += 1
            for rule in active_rules:
                if rule.column in row and not rule.predicate(row[rule.column]):
                    failures[rule.name] += 1
            if limit and rows >= limit:
                break

    total_checks = max(rows * len(active_rules), 1)
    failed_checks = sum(failures.values())
    score = round(100 * (1 - failed_checks / total_checks), 2)
    return {
        "dataset": str(path),
        "rows_checked": rows,
        "score": score,
        "failed_checks": failed_checks,
        "failures": failures,
    }

