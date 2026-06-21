from __future__ import annotations

from collections.abc import Iterable
from typing import TypeVar

from timeglance.forecast import ForecastIterator, forecast

T = TypeVar("T")


def forecast_partitions(partitions: Iterable[T], **kwargs: object) -> ForecastIterator[T]:
    return forecast(partitions, **kwargs)
