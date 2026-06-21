from __future__ import annotations

import json
from pathlib import Path

from timeglance.models.report import Report


def export_json(report: Report, path: str | Path) -> Path:
    target = Path(path)
    target.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    return target
