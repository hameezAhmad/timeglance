from __future__ import annotations

import csv
from pathlib import Path

from timeglance.models.report import Report


def export_csv(report: Report, path: str | Path) -> Path:
    target = Path(path)
    data = report.to_dict()["forecast"]
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(data.keys()))
        writer.writeheader()
        writer.writerow(data)
    return target
