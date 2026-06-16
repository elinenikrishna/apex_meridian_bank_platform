CREATE OR REPLACE VIEW warehouse.customer_360_mart AS
SELECT
    customer_id_hash,
    COUNT(*) AS transaction_count_90d,
    SUM(amount) AS transaction_amount_90d,
    COUNT(DISTINCT merchant_id) AS merchant_count_90d,
    MAX(event_ts) AS last_transaction_ts,
    SUM(CASE WHEN risk_band IN ('high', 'critical') THEN 1 ELSE 0 END) AS high_risk_transaction_count
FROM silver.card_transactions
WHERE event_ts >= CURRENT_DATE - INTERVAL '90 days'
GROUP BY customer_id_hash;

