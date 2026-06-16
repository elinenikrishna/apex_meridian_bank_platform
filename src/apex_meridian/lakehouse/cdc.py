from __future__ import annotations

import csv
from pathlib import Path


def apply_cdc_snapshot(base_file: Path, changes_file: Path, output_file: Path, key: str) -> Path:
    records: dict[str, dict] = {}
    if base_file.exists():
        with base_file.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                records[row[key]] = row

    fieldnames: list[str] | None = None
    with changes_file.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fieldnames = [name for name in reader.fieldnames or [] if name != "_cdc_operation"]
        for row in reader:
            operation = row.get("_cdc_operation", "upsert")
            row_key = row[key]
            if operation == "delete":
                records.pop(row_key, None)
            else:
                records[row_key] = {name: row.get(name, "") for name in fieldnames}

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames or [])
        writer.writeheader()
        writer.writerows(records.values())
    return output_file

