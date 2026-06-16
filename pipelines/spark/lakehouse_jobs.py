from __future__ import annotations

from pathlib import Path


def create_spark(app_name: str):
    from pyspark.sql import SparkSession

    return (
        SparkSession.builder.appName(app_name)
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.sql.shuffle.partitions", "96")
        .getOrCreate()
    )


def bronze_stream_transactions(kafka_bootstrap: str, bronze_path: str, checkpoint_path: str) -> None:
    spark = create_spark("apex-meridian-bronze-card-transactions")
    raw = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", kafka_bootstrap)
        .option("subscribe", "card.transactions.raw")
        .option("startingOffsets", "latest")
        .load()
    )
    (
        raw.selectExpr("CAST(key AS STRING) AS event_key", "CAST(value AS STRING) AS event_payload", "timestamp")
        .writeStream.format("delta")
        .option("checkpointLocation", checkpoint_path)
        .partitionBy("date")
        .trigger(processingTime="1 minute")
        .start(bronze_path)
    )


def bronze_to_silver_transactions(bronze_path: str, silver_path: str) -> None:
    from pyspark.sql import functions as F
    from pyspark.sql.types import BooleanType, DoubleType, IntegerType, StringType, StructField, StructType

    spark = create_spark("apex-meridian-silver-card-transactions")
    schema = StructType(
        [
            StructField("transaction_id", StringType()),
            StructField("customer_id", StringType()),
            StructField("account_id", StringType()),
            StructField("merchant_id", StringType()),
            StructField("event_ts", StringType()),
            StructField("amount", DoubleType()),
            StructField("currency", StringType()),
            StructField("merchant_category", StringType()),
            StructField("channel", StringType()),
            StructField("region", StringType()),
            StructField("authorization_status", StringType()),
            StructField("device_trust_score", DoubleType()),
            StructField("card_present", BooleanType()),
            StructField("risk_signal_count", IntegerType()),
        ]
    )
    raw = spark.read.format("delta").load(bronze_path)
    parsed = raw.select(F.from_json("event_payload", schema).alias("event")).select("event.*")
    silver = (
        parsed.dropDuplicates(["transaction_id"])
        .where("transaction_id IS NOT NULL AND customer_id IS NOT NULL AND amount >= 0")
        .withColumn("event_date", F.to_date("event_ts"))
        .withColumn(
            "risk_band",
            F.when((F.col("amount") > 900) | (F.col("risk_signal_count") >= 4), "high")
            .when(F.col("risk_signal_count") >= 2, "medium")
            .otherwise("low"),
        )
        .withColumn("customer_id_hash", F.sha2("customer_id", 256))
    )
    silver.write.format("delta").mode("overwrite").option("mergeSchema", "true").partitionBy("event_date").save(
        silver_path
    )


def silver_to_gold_fraud_kpis(silver_path: str, gold_path: str) -> None:
    from pyspark.sql import functions as F

    spark = create_spark("apex-meridian-gold-fraud-kpis")
    silver = spark.read.format("delta").load(silver_path)
    gold = (
        silver.groupBy("event_date", "region", "merchant_category")
        .agg(
            F.count("*").alias("transaction_count"),
            F.sum("amount").alias("transaction_amount"),
            F.sum(F.when(F.col("risk_band") == "high", 1).otherwise(0)).alias("high_risk_transactions"),
            F.avg("device_trust_score").alias("avg_device_trust_score"),
        )
        .withColumn(
            "risk_rate_bps",
            F.round(F.col("high_risk_transactions") * F.lit(10000) / F.greatest(F.col("transaction_count"), F.lit(1)), 2),
        )
    )
    gold.write.format("delta").mode("overwrite").partitionBy("event_date").save(gold_path)


def main() -> None:
    root = Path("data/lakehouse")
    bronze_to_silver_transactions(
        str(root / "bronze/card_transactions"),
        str(root / "silver/card_transactions"),
    )
    silver_to_gold_fraud_kpis(
        str(root / "silver/card_transactions"),
        str(root / "gold/fraud_daily_kpis"),
    )


if __name__ == "__main__":
    main()

