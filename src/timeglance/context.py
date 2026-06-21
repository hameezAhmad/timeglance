from __future__ import annotations

from types import TracebackType

from .utils.memory import current_memory_mb, peak_memory_mb
from .utils.timing import now


class ForecastSession:
    """Context manager that records elapsed time and memory for a code block."""

    def __init__(self) -> None:
        self.started_at: float | None = None
        self.elapsed: float = 0.0
        self.start_memory_mb: float = 0.0
        self.current_memory_mb: float = 0.0
        self.peak_memory_mb: float = 0.0

    def __enter__(self) -> "ForecastSession":
        self.started_at = now()
        self.start_memory_mb = current_memory_mb()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.elapsed = now() - (self.started_at or now())
        self.current_memory_mb = current_memory_mb()
        self.peak_memory_mb = peak_memory_mb()
