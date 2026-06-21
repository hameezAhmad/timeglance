from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from timeglance.forecast import ForecastIterator, forecast


def forecast_rows(frame: Any, **kwargs: object) -> ForecastIterator[tuple[Any, Any]]:
    return forecast(frame.iterrows(), **kwargs)


def forecast_records(records: Iterable[dict[str, Any]], **kwargs: object) -> ForecastIterator[dict[str, Any]]:
    return forecast(records, **kwargs)
