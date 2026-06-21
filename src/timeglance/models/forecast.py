from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Forecast:
    """A point-in-time prediction for an iterable workload."""

    completed: int
    total: int | None
    elapsed_seconds: float
    estimated_total_seconds: float | None
    eta_seconds: float | None
    throughput_per_second: float
    confidence: float
    current_memory_mb: float | None = None
    peak_memory_mb: float | None = None
    estimated_peak_memory_mb: float | None = None
    risk_level: str = "LOW"

    @property
    def progress(self) -> float | None:
        if not self.total:
            return None
        return min(1.0, self.completed / self.total)
