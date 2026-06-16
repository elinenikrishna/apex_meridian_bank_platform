from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(min_length=3, max_length=800)
    user_id: str = "executive-demo"
    role: str = "risk_executive"


class ChatResponse(BaseModel):
    answer: str
    confidence: float
    refused: bool
    citations: list[str]
    audit_event_id: str


class ReportRequest(BaseModel):
    report_type: str = "weekly_executive_risk"
    week_ending: str | None = None
    requested_by: str = "executive-demo"


class ReportResponse(BaseModel):
    report_id: str
    status: str
    generated_at: datetime
    validation_status: str
    sections: list[str]
    metrics_used: dict[str, Any]

