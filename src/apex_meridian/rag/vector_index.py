from __future__ import annotations

import json
import math
import re
from collections import Counter
from pathlib import Path

TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9_]+")


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_PATTERN.findall(text)]


class SimpleTfidfVectorIndex:
    def __init__(self) -> None:
        self.documents: list[dict] = []

    def add(self, doc_id: str, text: str, metadata: dict | None = None) -> None:
        self.documents.append({"doc_id": doc_id, "text": text, "metadata": metadata or {}})

    def search(self, query: str, limit: int = 4) -> list[dict]:
        query_tokens = Counter(tokenize(query))
        scored: list[tuple[float, dict]] = []
        for document in self.documents:
            doc_tokens = Counter(tokenize(document["text"]))
            score = cosine(query_tokens, doc_tokens)
            if score > 0:
                scored.append((score, document))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [
            {
                "score": round(score, 4),
                "doc_id": document["doc_id"],
                "text": document["text"],
                "metadata": document["metadata"],
            }
            for score, document in scored[:limit]
        ]

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as handle:
            json.dump({"documents": self.documents}, handle, indent=2)

    @classmethod
    def load(cls, path: Path) -> "SimpleTfidfVectorIndex":
        index = cls()
        if path.exists():
            with path.open(encoding="utf-8") as handle:
                payload = json.load(handle)
            index.documents = payload.get("documents", [])
        return index


def cosine(left: Counter, right: Counter) -> float:
    common = set(left) & set(right)
    numerator = sum(left[token] * right[token] for token in common)
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return numerator / (left_norm * right_norm)

