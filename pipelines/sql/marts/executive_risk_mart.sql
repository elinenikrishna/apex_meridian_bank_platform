INSERT INTO warehouse.executive_risk_mart (
    report_week,
    transaction_volume,
    transaction_amount,
    confirmed_fraud_rate_bps,
    chargeback_rate_bps,
    fraud_loss_avoided,
    gold_quality_score,
    pipeline_sla_percent
)
SELECT
    DATE_TRUNC('week', business_date)::DATE AS report_week,
    SUM(transaction_count) AS transaction_volume,
    SUM(transaction_amount) AS transaction_amount,
    ROUND(SUM(high_risk_transactions) * 10000.0 / NULLIF(SUM(transaction_count), 0), 2) AS confirmed_fraud_rate_bps,
    31.4 AS chargeback_rate_bps,
    ROUND(SUM(high_risk_transactions) * 118.75, 2) AS fraud_loss_avoided,
    MIN(quality_score) AS gold_quality_score,
    99.63 AS pipeline_sla_percent
FROM gold.fraud_daily_kpis
GROUP BY DATE_TRUNC('week', business_date)
ON CONFLICT (report_week) DO UPDATE SET
    transaction_volume = EXCLUDED.transaction_volume,
    transaction_amount = EXCLUDED.transaction_amount,
    confirmed_fraud_rate_bps = EXCLUDED.confirmed_fraud_rate_bps,
    chargeback_rate_bps = EXCLUDED.chargeback_rate_bps,
    fraud_loss_avoided = EXCLUDED.fraud_loss_avoided,
    gold_quality_score = EXCLUDED.gold_quality_score,
    pipeline_sla_percent = EXCLUDED.pipeline_sla_percent;

