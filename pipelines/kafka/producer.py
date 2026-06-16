from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from apex_meridian.data_generation.generator import transaction_record


def produce_transactions(topic: str, bootstrap_servers: str, count: int, delay_ms: int) -> None:
    try:
        from kafka import KafkaProducer

        producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda value: json.dumps(value).encode("utf-8"),
            key_serializer=lambda value: value.encode("utf-8"),
        )
    except Exception as exc:
        print(f"Kafka producer unavailable ({exc}); writing preview events to work/kafka_preview.jsonl")
        preview_path = Path("work/kafka_preview.jsonl")
        preview_path.parent.mkdir(parents=True, exist_ok=True)
        with preview_path.open("w", encoding="utf-8") as handle:
            import random

            rng = random.Random(421)
            for index in range(count):
                event = transaction_record(index, rng)
                handle.write(json.dumps({"topic": topic, "key": event["transaction_id"], "value": event}) + "\n")
        return

    import random

    rng = random.Random(421)
    for index in range(count):
        event = transaction_record(index, rng)
        producer.send(topic, key=event["transaction_id"], value=event)
        if delay_ms:
            time.sleep(delay_ms / 1000)
    producer.flush()


def main() -> None:
    parser = argparse.ArgumentParser(description="Produce Apex Meridian synthetic transaction events.")
    parser.add_argument("--topic", default="card.transactions.raw")
    parser.add_argument("--bootstrap-servers", default="localhost:9092")
    parser.add_argument("--count", type=int, default=1000)
    parser.add_argument("--delay-ms", type=int, default=0)
    args = parser.parse_args()
    produce_transactions(args.topic, args.bootstrap_servers, args.count, args.delay_ms)


if __name__ == "__main__":
    main()

