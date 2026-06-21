from __future__ import annotations

from html import escape
from pathlib import Path

from timeglance.models.report import Report


def export_html(report: Report, path: str | Path) -> Path:
    target = Path(path)
    rows = "\n".join(
        f"<tr><th>{escape(str(key))}</th><td>{escape(str(value))}</td></tr>"
        for key, value in report.to_dict()["forecast"].items()
    )
    target.write_text(
        f"<!doctype html><html><head><meta charset='utf-8'><title>TimeGlance Report</title>"
        f"<style>body{{font-family:system-ui,sans-serif;margin:2rem;}}"
        f"table{{border-collapse:collapse;}}th,td{{border:1px solid #ddd;padding:.5rem 1rem;}}</style>"
        f"</head><body><h1>TimeGlance Report</h1><table>{rows}</table></body></html>",
        encoding="utf-8",
    )
    return target
