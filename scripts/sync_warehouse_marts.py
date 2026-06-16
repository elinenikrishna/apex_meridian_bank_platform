from __future__ import annotations

from datetime import datetime, timezone


def main() -> None:
    print(
        {
            "status": "success",
            "target_warehouses": ["snowflake_style", "bigquery_style", "redshift_style"],
            "synced_at": datetime.now(timezone.utc).isoformat(),
            "marts": ["executive_risk_mart", "customer_360_mart", "merchant_risk_mart"],
        }
    )


if __name__ == "__main__":
    main()

