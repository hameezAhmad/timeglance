from __future__ import annotations

from .statistics import coefficient_of_variation


def confidence_from_durations(durations: list[float], sample_size: int | None = None) -> float:
    """Return a 0-1 confidence score from timing stability and sample count."""

    if not durations:
        return 0.0
    target = sample_size or max(len(durations), 1)
    sample_factor = min(1.0, len(durations) / target)
    stability = max(0.0, 1.0 - coefficient_of_variation(durations))
    return round(max(0.0, min(1.0, 0.35 * sample_factor + 0.65 * stability)), 4)
