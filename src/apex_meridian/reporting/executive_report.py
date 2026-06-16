from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path


def weekly_report_markdown(metrics: dict, citations: list[str]) -> str:
    return "\n".join(
        [
            "# Apex Meridian Weekly Executive Risk Report",
            "",
            f"Generated: {datetime.now(timezone.utc).isoformat()}",
            "",
            "## Executive Position",
            f"- Seven-day transaction volume: {metrics['transaction_volume_7d']:,}",
            f"- Fraud loss avoided: ${metrics['fraud_loss_avoided_7d']:,.2f}",
            f"- Confirmed fraud rate: {metrics['confirmed_fraud_rate_bps']} bps",
            f"- Gold data quality score: {metrics['gold_quality_score']}%",
            "",
            "## Governed Citations",
            *[f"- {citation}" for citation in citations],
        ]
    )


def write_report(metrics: dict, citations: list[str], output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    content = weekly_report_markdown(metrics, citations)
    if output_path.suffix.lower() == ".pdf":
        try:
            from reportlab.lib.pagesizes import LETTER
            from reportlab.pdfgen import canvas

            pdf = canvas.Canvas(str(output_path), pagesize=LETTER)
            width, height = LETTER
            y = height - 56
            for line in content.splitlines():
                pdf.drawString(56, y, line[:110])
                y -= 16
                if y < 56:
                    pdf.showPage()
                    y = height - 56
            pdf.save()
            return output_path
        except ImportError:
            output_path = output_path.with_suffix(".md")
    output_path.write_text(content, encoding="utf-8")
    return output_path

