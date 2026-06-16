from __future__ import annotations

from apex_meridian.config import get_config
from apex_meridian.governance.audit import AuditLogger
from apex_meridian.rag.chatbot import GovernedBankingChatbot
from apps.backend.app.services.catalog import snapshot


def answer_question(question: str, role: str, user_id: str) -> dict:
    bot = GovernedBankingChatbot.from_platform_snapshot(snapshot())
    response = bot.answer(question=question, role=role, user_id=user_id)
    AuditLogger(get_config().audit_log_path).emit(
        actor=f"api:{user_id}",
        action="ask_governed_chatbot",
        dataset=",".join(response["citations"]) or "unresolved_dataset_request",
        status="refused" if response["refused"] else "success",
        metadata={"role": role, "audit_event_id": response["audit_event_id"]},
    )
    return response
