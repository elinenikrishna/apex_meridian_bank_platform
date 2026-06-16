from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apps.backend.app.models import ChatRequest, ChatResponse, ReportRequest, ReportResponse
from apps.backend.app.services.catalog import snapshot
from apps.backend.app.services.chatbot_service import answer_question
from apps.backend.app.services.report_service import generate_executive_report

app = FastAPI(
    title="Apex Meridian Bank Intelligence Platform API",
    version="1.0.0",
    description="Governed banking analytics, fraud intelligence, lakehouse monitoring, and AI reporting APIs.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "apex-meridian-api"}


@app.get("/api/v1/dashboard/kpis")
def dashboard_kpis() -> dict:
    data = snapshot()
    return {"as_of": data["as_of"], "kpis": data["executive_kpis"]}


@app.get("/api/v1/transactions/analytics")
def transaction_analytics() -> dict:
    data = snapshot()
    return {
        "volume_7d": data["executive_kpis"]["transaction_volume_7d"],
        "amount_7d": data["executive_kpis"]["transaction_amount_7d"],
        "regional_patterns": data["fraud_metrics"]["regional_patterns"],
        "behavior_changes": data["customer_360"]["behavior_changes"],
    }


@app.get("/api/v1/fraud/metrics")
def fraud_metrics() -> dict:
    data = snapshot()
    return data["fraud_metrics"]


@app.get("/api/v1/customers/{customer_id}/risk-profile")
def customer_risk_profile(customer_id: str) -> dict:
    data = snapshot()
    risk_seed = sum(ord(char) for char in customer_id) % 100
    return {
        "customer_id": customer_id,
        "risk_score": max(12, min(96, risk_seed)),
        "segment": data["customer_360"]["segments"][risk_seed % len(data["customer_360"]["segments"])]["segment"],
        "signals": [
            "transaction_velocity",
            "merchant_category_shift",
            "chargeback_history",
            "device_consistency",
        ],
        "pii_policy": "Direct identifiers masked in analytics responses.",
    }


@app.get("/api/v1/data-quality/scorecards")
def data_quality_scorecards() -> dict:
    return snapshot()["data_quality"]


@app.get("/api/v1/pipelines/status")
def pipeline_status() -> dict:
    return snapshot()["pipeline_status"]


@app.post("/api/v1/ai/chat", response_model=ChatResponse)
def ai_chat(request: ChatRequest) -> ChatResponse:
    return ChatResponse(**answer_question(request.question, request.role, request.user_id))


@app.post("/api/v1/reports/generate", response_model=ReportResponse)
def report_generation(request: ReportRequest) -> ReportResponse:
    return ReportResponse(
        **generate_executive_report(
            report_type=request.report_type,
            requested_by=request.requested_by,
            week_ending=request.week_ending,
        )
    )


@app.get("/api/v1/audit/logs")
def audit_logs() -> dict:
    return {"events": snapshot()["audit_logs"]}


@app.get("/api/v1/lineage")
def lineage_metadata() -> dict:
    return snapshot()["lineage"]


@app.get("/api/v1/governance/policies")
def governance_policies() -> dict:
    return snapshot()["governance"]

