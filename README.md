# TimeGlance

Forecast runtime and memory usage while Python workloads are still running.

[![PyPI Version](https://img.shields.io/pypi/v/timeglance)](https://pypi.org/project/timeglance/)
[![Python Versions](https://img.shields.io/pypi/pyversions/timeglance)](https://pypi.org/project/timeglance/)
[![License](https://img.shields.io/github/license/hameezAhmad/timeglance)](LICENSE)

TimeGlance is a lightweight Python library for estimating how long an iterable
workload may take, how much memory it may use, and whether it is approaching
runtime or memory limits.

It is useful for data processing loops, batch jobs, experiments, and scripts
where a normal progress bar tells you what already happened, but you also want
an early read on what is likely to happen next.

## Features

- Runtime forecasting for synchronous iterables.
- Async iterable support with `aforecast`.
- Memory tracking using Python's built-in `tracemalloc`.
- Confidence scoring based on iteration timing stability.
- Risk levels for runtime and memory thresholds.
- JSON, CSV, and HTML report exports.
- Small dependency-free core with optional integrations.

## Installation

```bash
pip install timeglance
```

For local development:

```bash
git clone https://github.com/hameezAhmad/timeglance.git
cd timeglance
python -m pip install -e ".[dev]"
```

## Quick Start

```python
from timeglance import forecast

items = forecast(range(1000), sample_size=25, update_every=100)

for item in items:
    # do work here
    pass

print(items.latest)
```

`items.latest` contains a `Forecast` dataclass with fields such as:

- `eta_seconds`
- `estimated_total_seconds`
- `throughput_per_second`
- `confidence`
- `current_memory_mb`
- `estimated_peak_memory_mb`
- `risk_level`

## Runtime And Memory Limits

```python
from timeglance import forecast

items = forecast(
    range(50_000),
    sample_size=100,
    update_every=500,
    max_ram_mb=1024,
    max_time_sec=600,
)

for item in items:
    pass

print(items.latest.risk_level)
```

Risk levels are `LOW`, `MEDIUM`, `HIGH`, and `CRITICAL`.

## Async Usage

```python
import asyncio
from timeglance import aforecast


async def stream():
    for item in range(10):
        await asyncio.sleep(0.01)
        yield item


async def main():
    async for item in aforecast(stream(), sample_size=3):
        print(item)


asyncio.run(main())
```

## Export Reports

TimeGlance can write the final forecast to JSON, CSV, or HTML.

```python
from timeglance import forecast

for item in forecast(range(100), export="timeglance-report.json"):
    pass
```

The export format is selected from the file extension:

- `.json`
- `.csv`
- `.html` or `.htm`

## Context Manager

Use `ForecastSession` when you want timing and memory measurements for a block
instead of an iterable.

```python
from timeglance import ForecastSession

with ForecastSession() as session:
    result = sum(range(1_000_000))

print(session.elapsed)
print(session.peak_memory_mb)
```

## Decorator

```python
from timeglance import forecast_function


@forecast_function
def train_model():
    return "done"


train_model()
print(train_model.latest_session.elapsed)
```

## Optional Integrations

The core package has no required third-party runtime dependencies. Optional
extras are available for users who want ecosystem-specific helpers:

```bash
pip install "timeglance[rich]"
pip install "timeglance[pandas]"
pip install "timeglance[numpy]"
pip install "timeglance[dask]"
```

## Development

Run tests:

```bash
pytest
```

Build distributions:

```bash
python -m build
twine check dist/*
```

## Project Status

TimeGlance is early-stage software. The public API is intentionally small and
focused on reliable primitives that can grow into richer dashboards and
framework integrations.

## License

MIT License. See [LICENSE](LICENSE).
