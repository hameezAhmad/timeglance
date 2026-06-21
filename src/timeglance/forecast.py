from __future__ import annotations

import time
from collections.abc import AsyncIterable, AsyncIterator, Iterable, Iterator
from typing import TypeVar

from .config import ForecastConfig
from .models.forecast import Forecast
from .predictor import build_forecast
from .reporter import export_report
from .utils.memory import current_memory_mb, peak_memory_mb
from .utils.timing import now

T = TypeVar("T")


def _total(iterable: Iterable[T]) -> int | None:
    try:
        return len(iterable)  # type: ignore[arg-type]
    except TypeError:
        return None


class ForecastIterator(Iterator[T]):
    def __init__(self, iterable: Iterable[T], config: ForecastConfig):
        self._iterator = iter(iterable)
        self._total = _total(iterable)
        self._config = config.validate()
        self._completed = 0
        self._durations: list[float] = []
        self._started = now()
        self._last_item_started = self._started
        self._baseline_memory = current_memory_mb()
        self.latest: Forecast | None = None

    def __iter__(self) -> "ForecastIterator[T]":
        return self

    def __next__(self) -> T:
        try:
            item = next(self._iterator)
        except StopIteration:
            self._finalize()
            raise

        item_started = now()
        if self._completed:
            self._durations.append(item_started - self._last_item_started)
        self._completed += 1
        self._last_item_started = item_started
        if self._should_update:
            self.latest = self.snapshot()
        return item

    @property
    def _should_update(self) -> bool:
        return (
            self._completed <= self._config.sample_size
            or self._completed % self._config.update_every == 0
            or self._completed == self._total
        )

    def snapshot(self) -> Forecast:
        return build_forecast(
            completed=self._completed,
            total=self._total,
            elapsed_seconds=now() - self._started,
            durations=self._durations,
            current_memory_mb=current_memory_mb(),
            peak_memory_mb=peak_memory_mb(),
            baseline_memory_mb=self._baseline_memory,
            sample_size=self._config.sample_size,
            max_time_sec=self._config.max_time_sec,
            max_ram_mb=self._config.max_ram_mb,
        )

    def _finalize(self) -> None:
        if self.latest is None or self.latest.completed != self._completed:
            self.latest = self.snapshot()
        if self._config.export:
            export_report(self.latest, self._config.export)


def forecast(
    iterable: Iterable[T],
    *,
    sample_size: int = 20,
    update_every: int = 100,
    max_ram_mb: float | None = None,
    max_time_sec: float | None = None,
    export: str | None = None,
) -> ForecastIterator[T]:
    """Yield items while collecting runtime and memory forecast data."""

    return ForecastIterator(
        iterable,
        ForecastConfig(
            sample_size=sample_size,
            update_every=update_every,
            max_ram_mb=max_ram_mb,
            max_time_sec=max_time_sec,
            export=export,
        ),
    )


async def aforecast(
    iterable: AsyncIterable[T],
    *,
    sample_size: int = 20,
    update_every: int = 100,
    max_ram_mb: float | None = None,
    max_time_sec: float | None = None,
    export: str | None = None,
) -> AsyncIterator[T]:
    config = ForecastConfig(sample_size, update_every, max_ram_mb, max_time_sec, export).validate()
    completed = 0
    durations: list[float] = []
    started = now()
    last_item_started = started
    baseline_memory = current_memory_mb()
    latest: Forecast | None = None

    async for item in iterable:
        item_started = now()
        if completed:
            durations.append(item_started - last_item_started)
        completed += 1
        last_item_started = item_started
        if completed <= config.sample_size or completed % config.update_every == 0:
            latest = build_forecast(
                completed=completed,
                total=None,
                elapsed_seconds=now() - started,
                durations=durations,
                current_memory_mb=current_memory_mb(),
                peak_memory_mb=peak_memory_mb(),
                baseline_memory_mb=baseline_memory,
                sample_size=config.sample_size,
                max_time_sec=config.max_time_sec,
                max_ram_mb=config.max_ram_mb,
            )
        yield item

    latest = latest or build_forecast(
        completed=completed,
        total=None,
        elapsed_seconds=time.perf_counter() - started,
        durations=durations,
        current_memory_mb=current_memory_mb(),
        peak_memory_mb=peak_memory_mb(),
        baseline_memory_mb=baseline_memory,
        sample_size=config.sample_size,
        max_time_sec=config.max_time_sec,
        max_ram_mb=config.max_ram_mb,
    )
    if config.export:
        export_report(latest, config.export)
