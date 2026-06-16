from __future__ import annotations

from pathlib import Path

from apps.backend.app.services.catalog import PLATFORM_SNAPSHOT
from apex_meridian.reporting.executive_report import write_report


def main() -> None:
    output = write_report(
        PLATFORM_SNAPSHOT["executive_kpis"],
        ["gold.fraud_daily_kpis", "warehouse.executive_risk_mart", "gold.data_quality_scorecards"],
        Path("outputs/apex_meridian_weekly_risk_report.pdf"),
    )
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()

