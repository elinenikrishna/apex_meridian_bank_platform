from __future__ import annotations

import hashlib
from collections.abc import Mapping
from typing import Any

PII_FIELDS = {"full_name", "email", "phone", "ssn_token", "address", "date_of_birth"}


def tokenise(value: str, salt: str = "apex-meridian") -> str:
    digest = hashlib.sha256(f"{salt}:{value}".encode("utf-8")).hexdigest()
    return f"tok_{digest[:24]}"


def mask_email(value: str) -> str:
    if "@" not in value:
        return "***"
    local, domain = value.split("@", 1)
    return f"{local[:2]}***@{domain}"


def mask_phone(value: str) -> str:
    digits = "".join(char for char in value if char.isdigit())
    return f"***-***-{digits[-4:]}" if len(digits) >= 4 else "***"


def mask_record(record: Mapping[str, Any]) -> dict[str, Any]:
    masked: dict[str, Any] = {}
    for key, value in record.items():
        if key == "email":
            masked[key] = mask_email(str(value))
        elif key == "phone":
            masked[key] = mask_phone(str(value))
        elif key in {"full_name", "ssn_token", "address", "date_of_birth"}:
            masked[key] = tokenise(str(value))
        else:
            masked[key] = value
    return masked

