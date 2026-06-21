from pathlib import Path

import pytest

from timeglance import ForecastSession, forecast, forecast_function
from timeglance.exceptions import ExportError, ForecastConfigurationError
from timeglance.reporter import export_report


def test_forecast_iterates_and_records_latest():
    items = forecast(range(5), sample_size=2, update_every=1)

    assert list(items) == [0, 1, 2, 3, 4]
    assert items.latest is not None
    assert items.latest.completed == 5
    assert items.latest.total == 5
    assert items.latest.progress == 1.0
    assert items.latest.throughput_per_second >= 0
    assert 0 <= items.latest.confidence <= 1


def test_forecast_exports_json(tmp_path: Path):
    target = tmp_path / "report.json"
    items = forecast(range(3), export=str(target))

    assert list(items) == [0, 1, 2]
    assert target.exists()
    assert "estimated_total_seconds" in target.read_text(encoding="utf-8")


def test_forecast_rejects_invalid_config():
    with pytest.raises(ForecastConfigurationError):
        forecast(range(1), sample_size=0)


def test_export_rejects_unknown_extension(tmp_path: Path):
    items = forecast(range(1))
    list(items)

    with pytest.raises(ExportError):
        export_report(items.latest, tmp_path / "report.txt")


def test_context_manager_records_elapsed_time():
    with ForecastSession() as session:
        sum(range(100))

    assert session.elapsed >= 0
    assert session.peak_memory_mb >= 0


def test_forecast_function_attaches_latest_session():
    @forecast_function
    def work():
        return "ok"

    assert work() == "ok"
    assert work.latest_session is not None
    assert work.latest_session.elapsed >= 0
