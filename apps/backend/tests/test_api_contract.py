import pytest

fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient

from apps.backend.app.main import app


def test_dashboard_kpis_contract():
    client = TestClient(app)
    response = client.get("/api/v1/dashboard/kpis")
    assert response.status_code == 200
    body = response.json()
    assert body["kpis"]["transaction_volume_7d"] > 0
    assert body["kpis"]["gold_quality_score"] >= 90


def test_chatbot_refuses_unsupported_questions():
    client = TestClient(app)
    response = client.post(
        "/api/v1/ai/chat",
        json={"question": "What is the CEO's private phone number?", "role": "risk_executive"},
    )
    assert response.status_code == 200
    assert response.json()["refused"] is True
