# Data Model

## Source Domains

| Domain | Grain | Primary Key | Notes |
| --- | --- | --- | --- |
| Customer Profiles | Customer snapshot | `customer_id` | KYC, segment, region, masked PII |
| Card Transactions | Authorization event | `transaction_id` | Amount, channel, merchant, risk signals |
| Merchant Activity | Merchant event | `merchant_id`, `event_ts` | Category, onboarding tier, region |
| Loan Payments | Payment event | `payment_id` | Principal, interest, delinquency |
| Rewards Activity | Reward event | `reward_event_id` | Earn, redeem, program |
| Fraud Alerts | Alert event | `alert_id` | Alert type, score, case status |
| Chargebacks | Dispute event | `chargeback_id` | Reason, amount, status |

## Lakehouse Tables

### Bronze

- `bronze.card_transactions_raw`
- `bronze.customer_profiles_raw`
- `bronze.merchant_events_raw`
- `bronze.loan_payments_raw`
- `bronze.rewards_events_raw`
- `bronze.fraud_alerts_raw`
- `bronze.chargebacks_raw`

### Silver

- `silver.card_transactions`
- `silver.customer_profiles_masked`
- `silver.merchants`
- `silver.loan_payments`
- `silver.rewards_activity`
- `silver.fraud_alerts`
- `silver.chargebacks`

### Gold

- `gold.fraud_daily_kpis`
- `gold.customer_360`
- `gold.merchant_risk_kpis`
- `gold.chargeback_kpis`
- `gold.pipeline_observability`
- `gold.data_quality_scorecards`
- `gold.regulatory_weekly_risk_report`

## Warehouse Marts

- `warehouse.executive_risk_mart`
- `warehouse.customer_360_mart`
- `warehouse.merchant_risk_mart`
- `warehouse.regulatory_reporting_mart`

## PII Handling

Direct identifiers are masked or tokenized before Silver publication. Gold and warehouse layers expose only aggregated, masked, or hashed identifiers unless a role-based exception is approved.

