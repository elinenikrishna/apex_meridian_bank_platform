CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;
CREATE SCHEMA IF NOT EXISTS warehouse;
CREATE SCHEMA IF NOT EXISTS governance;

CREATE TABLE IF NOT EXISTS silver.card_transactions (
    transaction_id          VARCHAR(40) PRIMARY KEY,
    customer_id_hash        VARCHAR(128) NOT NULL,
    account_id              VARCHAR(40) NOT NULL,
    merchant_id             VARCHAR(40) NOT NULL,
    event_ts                TIMESTAMP NOT NULL,
    event_date              DATE NOT NULL,
    amount                  NUMERIC(18, 2) NOT NULL,
    currency                CHAR(3) NOT NULL,
    merchant_category       VARCHAR(120) NOT NULL,
    channel                 VARCHAR(40) NOT NULL,
    region                  VARCHAR(40) NOT NULL,
    authorization_status    VARCHAR(30) NOT NULL,
    risk_band               VARCHAR(20) NOT NULL,
    loaded_at               TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS gold.fraud_daily_kpis (
    business_date           DATE NOT NULL,
    region                  VARCHAR(40) NOT NULL,
    merchant_category       VARCHAR(120) NOT NULL,
    transaction_count       BIGINT NOT NULL,
    transaction_amount      NUMERIC(22, 2) NOT NULL,
    high_risk_transactions  BIGINT NOT NULL,
    risk_rate_bps           NUMERIC(10, 2) NOT NULL,
    quality_score           NUMERIC(5, 2) NOT NULL,
    PRIMARY KEY (business_date, region, merchant_category)
);

CREATE TABLE IF NOT EXISTS warehouse.executive_risk_mart (
    report_week             DATE PRIMARY KEY,
    transaction_volume      BIGINT NOT NULL,
    transaction_amount      NUMERIC(22, 2) NOT NULL,
    confirmed_fraud_rate_bps NUMERIC(10, 2) NOT NULL,
    chargeback_rate_bps     NUMERIC(10, 2) NOT NULL,
    fraud_loss_avoided      NUMERIC(22, 2) NOT NULL,
    gold_quality_score      NUMERIC(5, 2) NOT NULL,
    pipeline_sla_percent    NUMERIC(5, 2) NOT NULL,
    created_at              TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS governance.ai_answer_audit (
    audit_event_id          VARCHAR(64) PRIMARY KEY,
    user_id                 VARCHAR(120) NOT NULL,
    role_name               VARCHAR(80) NOT NULL,
    question_hash           VARCHAR(128) NOT NULL,
    refused                 BOOLEAN NOT NULL,
    citations               TEXT NOT NULL,
    prompt_version          VARCHAR(80) NOT NULL,
    created_at              TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

