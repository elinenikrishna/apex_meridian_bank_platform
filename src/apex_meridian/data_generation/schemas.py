from __future__ import annotations

TRANSACTION_COLUMNS = [
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
]

CUSTOMER_COLUMNS = [
    "customer_id",
    "full_name",
    "email",
    "phone",
    "ssn_token",
    "segment",
    "home_region",
    "opened_date",
    "kyc_status",
    "annual_income_band",
]

MERCHANT_COLUMNS = [
    "merchant_id",
    "merchant_name",
    "merchant_category",
    "region",
    "onboarding_risk_tier",
    "active_since",
]

LOAN_PAYMENT_COLUMNS = [
    "payment_id",
    "loan_id",
    "customer_id",
    "event_ts",
    "amount",
    "principal_component",
    "interest_component",
    "days_past_due",
    "payment_channel",
]

REWARDS_COLUMNS = [
    "reward_event_id",
    "customer_id",
    "transaction_id",
    "event_ts",
    "points_earned",
    "points_redeemed",
    "reward_program",
]

FRAUD_ALERT_COLUMNS = [
    "alert_id",
    "transaction_id",
    "customer_id",
    "event_ts",
    "alert_type",
    "alert_score",
    "case_status",
    "analyst_queue",
]

CHARGEBACK_COLUMNS = [
    "chargeback_id",
    "transaction_id",
    "customer_id",
    "merchant_id",
    "event_ts",
    "dispute_reason",
    "amount",
    "status",
]

ACCOUNT_BALANCE_COLUMNS = [
    "balance_id",
    "account_id",
    "customer_id",
    "snapshot_date",
    "ledger_balance",
    "available_balance",
    "currency",
    "account_type",
    "region",
]

RISK_SCORE_COLUMNS = [
    "risk_score_id",
    "customer_id",
    "snapshot_date",
    "credit_risk_score",
    "fraud_risk_score",
    "aml_risk_score",
    "model_version",
    "reason_codes",
]

REGULATORY_REPORT_COLUMNS = [
    "report_id",
    "business_date",
    "report_type",
    "metric_name",
    "metric_value",
    "source_dataset",
    "control_status",
]

DOMAIN_COLUMNS = {
    "transactions": TRANSACTION_COLUMNS,
    "customers": CUSTOMER_COLUMNS,
    "merchants": MERCHANT_COLUMNS,
    "loan_payments": LOAN_PAYMENT_COLUMNS,
    "rewards": REWARDS_COLUMNS,
    "fraud_alerts": FRAUD_ALERT_COLUMNS,
    "chargebacks": CHARGEBACK_COLUMNS,
    "account_balances": ACCOUNT_BALANCE_COLUMNS,
    "risk_scores": RISK_SCORE_COLUMNS,
    "regulatory_reports": REGULATORY_REPORT_COLUMNS,
}
