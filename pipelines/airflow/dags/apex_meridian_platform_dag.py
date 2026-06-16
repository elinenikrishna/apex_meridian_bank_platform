from __future__ import annotations

from datetime import datetime, timedelta

try:
    from airflow import DAG
    from airflow.operators.bash import BashOperator
    from airflow.operators.python import PythonOperator
except ImportError:
    DAG = None


def _emit_governance_audit(**context) -> None:
    from apex_meridian.config import get_config
    from apex_meridian.governance.audit import AuditLogger

    config = get_config()
    AuditLogger(config.audit_log_path).emit(
        actor="airflow:governance_audit_export",
        action="export_governance_controls",
        dataset="gold.data_quality_scorecards",
        status="success",
        metadata={"run_id": context.get("run_id")},
    )


if DAG is not None:
    default_args = {
        "owner": "apex-meridian-data-platform",
        "depends_on_past": False,
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
        "email_on_failure": False,
    }

    with DAG(
        dag_id="apex_meridian_banking_lakehouse",
        description="Daily enterprise banking ingestion, lakehouse processing, fraud scoring, AI reporting, and governance export.",
        start_date=datetime(2026, 1, 1),
        schedule="@daily",
        catchup=False,
        max_active_runs=1,
        default_args=default_args,
        tags=["banking", "lakehouse", "fraud", "governance", "ai"],
    ) as dag:
        daily_batch_ingestion = BashOperator(
            task_id="daily_batch_ingestion",
            bash_command="python -m apex_meridian.data_generation.generator --records 50000 --batch-size 10000 --domains transactions,customers,merchants,loan_payments,rewards,fraud_alerts --output data/generated/airflow_batch",
        )

        stream_checkpoint_validation = BashOperator(
            task_id="stream_checkpoint_validation",
            bash_command="python pipelines/kafka/stream_checkpoint_validator.py",
        )

        bronze_to_silver = BashOperator(
            task_id="bronze_to_silver_transformation",
            bash_command="spark-submit pipelines/spark/lakehouse_jobs.py --stage bronze_to_silver",
        )

        data_quality_validation = BashOperator(
            task_id="data_quality_validation",
            bash_command="python scripts/run_quality_scorecards.py",
        )

        silver_to_gold = BashOperator(
            task_id="silver_to_gold_transformation",
            bash_command="spark-submit pipelines/spark/lakehouse_jobs.py --stage silver_to_gold",
        )

        fraud_model_scoring = BashOperator(
            task_id="fraud_model_scoring",
            bash_command="python scripts/score_fraud_sample.py",
        )

        ai_report_generation = BashOperator(
            task_id="ai_report_generation",
            bash_command="python scripts/generate_weekly_report.py",
        )

        governance_audit_export = PythonOperator(
            task_id="governance_audit_export",
            python_callable=_emit_governance_audit,
        )

        warehouse_sync = BashOperator(
            task_id="warehouse_synchronization",
            bash_command="python scripts/sync_warehouse_marts.py",
        )

        (
            daily_batch_ingestion
            >> stream_checkpoint_validation
            >> bronze_to_silver
            >> data_quality_validation
            >> silver_to_gold
            >> fraud_model_scoring
            >> ai_report_generation
            >> governance_audit_export
            >> warehouse_sync
        )

