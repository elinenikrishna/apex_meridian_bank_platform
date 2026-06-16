CREATE TABLE IF NOT EXISTS gold.data_quality_scorecards (
    scorecard_date DATE NOT NULL,
    dataset_name VARCHAR(160) NOT NULL,
    completeness_score NUMERIC(5, 2) NOT NULL,
    validity_score NUMERIC(5, 2) NOT NULL,
    freshness_minutes INTEGER NOT NULL,
    failed_rules INTEGER NOT NULL,
    PRIMARY KEY (scorecard_date, dataset_name)
);

INSERT INTO gold.data_quality_scorecards VALUES
    (CURRENT_DATE, 'gold.fraud_daily_kpis', 99.40, 98.80, 11, 0),
    (CURRENT_DATE, 'gold.customer_360', 98.70, 98.90, 22, 1),
    (CURRENT_DATE, 'silver.card_transactions', 97.90, 96.80, 7, 3)
ON CONFLICT (scorecard_date, dataset_name) DO NOTHING;

