from __future__ import annotations

from timeglance.display.terminal import render_forecast
from timeglance.models.forecast import Forecast


def print_forecast(forecast: Forecast) -> None:
    try:
        from rich.console import Console
        from rich.panel import Panel

        Console().print(Panel(render_forecast(forecast), title="TimeGlance"))
    except Exception:
        print(render_forecast(forecast))
