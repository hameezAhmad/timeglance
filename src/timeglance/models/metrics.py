from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Metrics:
    """Observed measurements collected during an iteration session."""

    completed: int
    total: int | None
    elapsed_seconds: float
    average_item_seconds: float
    throughput_per_second: float
    current_memory_mb: float | None = None
    peak_memory_mb: float | None = None
