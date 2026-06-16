# AI Governance

## Principles

The AI reporting layer is designed for governed banking analytics. It does not answer from raw data, unapproved Silver tables, user memory, or unsupported assumptions.

## Controls

- **Gold-only retrieval:** Answers are built from approved Gold metrics and governed metadata.
- **Citations:** Each answer returns dataset citations.
- **Refusal:** Unsupported questions are refused with the dataset needed to answer.
- **Prompt versioning:** `PROMPT_VERSION` identifies report and chatbot policy versions.
- **RBAC alignment:** Role-to-dataset access lives in [data/reference/rbac_policies.json](data/reference/rbac_policies.json).
- **Hallucination checks:** The chatbot requires retrieved context before generating a response.
- **Audit trail:** Each answer receives an audit event ID.

## Supported Questions

- Weekly fraud trends
- High-risk merchant categories
- Transaction volume changes
- Customer segment behavior
- Chargeback spikes
- Regional risk patterns
- Data quality issues
- Pipeline failures
- KPI explanation

## Unsupported Questions

The chatbot refuses direct PII, personnel secrets, unindexed topics, non-governed metrics, and questions requiring datasets absent from the approved catalog.

