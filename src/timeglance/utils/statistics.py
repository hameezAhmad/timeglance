from __future__ import annotations

from statistics import fmean, pstdev
from typing import Iterable


def mean(values: Iterable[float]) -> float:
    items = list(values)
    return fmean(items) if items else 0.0


def coefficient_of_variation(values: Iterable[float]) -> float:
    items = list(values)
    if len(items) < 2:
        return 0.0
    avg = fmean(items)
    if avg == 0:
        return 0.0
    return pstdev(items) / avg
