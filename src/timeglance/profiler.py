from __future__ import annotations

from .models.forecast import Forecast
from .predictor import build_forecast
from .utils.memory import current_memory_mb, peak_memory_mb
from .utils.timing import now


class Profiler:
    """Low-level profiler for callers that want manual checkpointing."""

    def __init__(self, total: int | None = None, sample_size: int = 20):
        self.total = total
        self.sample_size = sample_size
        self.started = now()
        self.last = self.started
        self.completed = 0
        self.durations: list[float] = []
        self.baseline_memory_mb = current_memory_mb()

    def checkpoint(self, count: int = 1) -> Forecast:
        timestamp = now()
        if self.completed:
            self.durations.append(timestamp - self.last)
        self.completed += count
        self.last = timestamp
        return build_forecast(
            completed=self.completed,
            total=self.total,
            elapsed_seconds=timestamp - self.started,
            durations=self.durations,
            current_memory_mb=current_memory_mb(),
            peak_memory_mb=peak_memory_mb(),
            baseline_memory_mb=self.baseline_memory_mb,
            sample_size=self.sample_size,
        )
