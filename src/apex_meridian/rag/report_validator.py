from __future__ import annotations

import re

NUMBER_PATTERN = re.compile(r"\$?[0-9][0-9,]*(?:\.[0-9]+)?%?")


def validate_report_against_metrics(report_text: str, metrics: dict) -> dict:
    metric_values = {
        str(value).replace(",", "").replace("$", "").replace("%", "")
        for value in metrics.values()
        if isinstance(value, (int, float, str))
    }
    unsupported_numbers = []
    for match in NUMBER_PATTERN.findall(report_text):
        normalized = match.replace(",", "").replace("$", "").replace("%", "")
        if normalized not in metric_values and len(normalized) > 2:
            unsupported_numbers.append(match)

    return {
        "status": "passed" if not unsupported_numbers else "review_required",
        "unsupported_numbers": unsupported_numbers,
        "metric_count": len(metric_values),
    }

