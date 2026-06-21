from __future__ import annotations

import time
from contextlib import contextmanager
from typing import Callable, Iterator


def now() -> float:
    return time.perf_counter()


def format_seconds(seconds: float | None) -> str:
    if seconds is None:
        return "unknown"
    seconds = max(0, int(round(seconds)))
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours}h {minutes}m {secs}s"
    if minutes:
        return f"{minutes}m {secs}s"
    return f"{secs}s"


@contextmanager
def timer() -> Iterator[Callable[[], float]]:
    start = now()
    yield lambda: now() - start
