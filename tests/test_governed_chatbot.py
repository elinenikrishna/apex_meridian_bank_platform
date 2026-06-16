from apps.backend.app.services.catalog import snapshot
from apex_meridian.rag.chatbot import GovernedBankingChatbot


def test_chatbot_answers_from_gold_context():
    bot = GovernedBankingChatbot.from_platform_snapshot(snapshot())
    answer = bot.answer("What are the weekly fraud trends?")
    assert answer["refused"] is False
    assert "gold.fraud_daily_kpis" in answer["citations"]


def test_chatbot_refuses_unindexed_topic():
    bot = GovernedBankingChatbot.from_platform_snapshot(snapshot())
    answer = bot.answer("Tell me an employee password")
    assert answer["refused"] is True

