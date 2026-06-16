from __future__ import annotations


def build_fraud_features(spark, transactions_path: str, alerts_path: str, output_path: str) -> None:
    from pyspark.sql import functions as F

    tx = spark.read.format("delta").load(transactions_path)
    alerts = spark.read.format("delta").load(alerts_path)
    features = (
        tx.join(alerts.select("transaction_id", "alert_score", "case_status"), "transaction_id", "left")
        .withColumn("amount_log", F.log1p("amount"))
        .withColumn("is_confirmed_fraud", F.when(F.col("case_status") == "confirmed", 1).otherwise(0))
        .withColumn(
            "velocity_bucket",
            F.when(F.col("risk_signal_count") >= 4, "elevated")
            .when(F.col("risk_signal_count") >= 2, "watch")
            .otherwise("baseline"),
        )
    )
    features.write.format("delta").mode("overwrite").partitionBy("event_date").save(output_path)

