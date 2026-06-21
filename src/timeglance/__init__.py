"""TimeGlance: lightweight runtime and memory forecasting for Python loops."""

from .context import ForecastSession
from .decorators import forecast_function
from .forecast import ForecastIterator, aforecast, forecast
from .models.forecast import Forecast
from .profiler import Profiler

__version__ = "0.1.0"

__all__ = [
    "Forecast",
    "ForecastIterator",
    "ForecastSession",
    "Profiler",
    "__version__",
    "aforecast",
    "forecast",
    "forecast_function",
]
