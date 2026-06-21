from __future__ import annotations

from pathlib import Path

from .exceptions import ExportError
from .exporters.csv_exporter import export_csv
from .exporters.html_exporter import export_html
from .exporters.json_exporter import export_json
from .models.forecast import Forecast
from .models.report import Report


def export_report(forecast: Forecast, path: str | Path) -> Path:
    target = Path(path)
    report = Report.from_forecast(forecast)
    suffix = target.suffix.lower()
    if suffix == ".json":
        return export_json(report, target)
    if suffix == ".csv":
        return export_csv(report, target)
    if suffix in {".html", ".htm"}:
        return export_html(report, target)
    raise ExportError(f"Unsupported export format: {suffix or '<none>'}")
