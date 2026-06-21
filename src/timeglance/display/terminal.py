from __future__ import annotations

from timeglance.models.forecast import Forecast
from timeglance.utils.timing import format_seconds


def render_forecast(forecast: Forecast) -> str:
    return "\n".join(
        [
            "TimeGlance Forecast",
            f"Completed: {forecast.completed}/{forecast.total or '?'}",
            f"ETA: {format_seconds(forecast.eta_seconds)}",
            f"Confidence: {forecast.confidence:.0%}",
            f"Throughput: {forecast.throughput_per_second:.2f} items/s",
            f"Risk: {forecast.risk_level}",
        ]
    )
