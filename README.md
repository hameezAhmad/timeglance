# TimeGlance

> Forecast runtime and memory usage before your loop finishes.

[![PyPI Version](https://img.shields.io/pypi/v/timeglance)](https://pypi.org/project/timeglance/)
[![Python Versions](https://img.shields.io/pypi/pyversions/timeglance)](https://pypi.org/project/timeglance/)
[![License](https://img.shields.io/github/license/yourusername/timeglance)](LICENSE)

TimeGlance is a lightweight forecasting library that predicts **runtime**, **memory growth**, and **execution risk** early in iterable execution.

Unlike traditional progress bars and profilers that tell you what has already happened, TimeGlance predicts what is likely to happen before your workload finishes.

---

## Why TimeGlance?

Most monitoring tools answer:

> How much work has already completed?

TimeGlance answers:

> How long will this take and how much memory will it consume if it continues?

### Comparison

| Tool            | Progress | ETA | Memory Monitoring | Memory Forecasting | Runtime Forecasting |
| --------------- | -------- | --- | ----------------- | ------------------ | ------------------- |
| tqdm            | ✅        | ✅   | ❌                 | ❌                  | Partial             |
| Rich Progress   | ✅        | ✅   | ❌                 | ❌                  | Partial             |
| memory_profiler | ❌        | ❌   | ✅                 | ❌                  | ❌                   |
| psutil          | ❌        | ❌   | ✅                 | ❌                  | ❌                   |
| TimeGlance      | ✅        | ✅   | ✅                 | ✅                  | ✅                   |

---

# Features

## Runtime Forecasting

Predict execution time after sampling only a fraction of iterations.

```python
from timeglance import forecast

for item in forecast(data):
    process(item)
```

Output:

```text
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TimeGlance Forecast

ETA:            4m 23s
Confidence:     95%
Throughput:     452 items/sec

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Memory Forecasting

Estimate future memory consumption before dangerous growth occurs.

```python
for row in forecast(
    dataset,
    max_ram_mb=1024
):
    process(row)
```

Output:

```text
Estimated Memory: 1.8 GB

⚠ Predicted memory limit exceeded
```

---

## Confidence Scoring

Predictions include a confidence score derived from timing variance.

```text
Confidence: 97%
```

Higher confidence indicates more stable iteration behavior.

---

## Adaptive Forecasting

Continuously refine predictions during execution.

```python
forecast(
    data,
    sample_size=100,
    update_every=1000
)
```

---

## Rich Terminal Dashboard

Beautiful terminal output powered by Rich.

```text
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃       TimeGlance            ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ ETA          3m 12s         ┃
┃ Memory       824 MB         ┃
┃ Confidence   94%            ┃
┃ Speed        583/s          ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

---

## Risk Detection

TimeGlance classifies execution risk.

```text
Risk Level: LOW
```

Possible values:

* LOW
* MEDIUM
* HIGH
* CRITICAL

---

## Async Support

```python
from timeglance import aforecast

async for item in aforecast(stream):
    await process(item)
```

---

## Context Manager

```python
from timeglance import ForecastSession

with ForecastSession() as session:
    expensive_operation()

print(session.elapsed)
print(session.peak_memory_mb)
```

---

## Decorators

```python
from timeglance import forecast_function

@forecast_function
def train_model():
    ...
```

---

## Export Reports

### JSON

```python
forecast(
    data,
    export="report.json"
)
```

### CSV

```python
forecast(
    data,
    export="report.csv"
)
```

### HTML

```python
forecast(
    data,
    export="report.html"
)
```

---

# Installation

## PyPI

```bash
pip install timeglance
```

## Development Installation

```bash
git clone https://github.com/yourusername/timeglance.git

cd timeglance

pip install -e .
```

---

# Quick Start

```python
from timeglance import forecast

for item in forecast(
    range(100000),
    sample_size=100
):
    pass
```

---

# Advanced Example

```python
from timeglance import forecast

for row in forecast(
        dataset,
        sample_size=200,
        update_every=5000,
        max_ram_mb=1024,
        max_time_sec=600,
        export="forecast.json"
):
    process(row)
```

Output:

```text
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TimeGlance Forecast

ETA:                8m 31s
Estimated Memory:   743 MB
Confidence:         96%
Throughput:         813 items/s

Risk: LOW

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

# Project Structure

```text
timeglance/

├── pyproject.toml
├── README.md
├── LICENSE
├── CHANGELOG.md

├── src/
│   └── timeglance/
│
│       ├── __init__.py
│       ├── forecast.py
│       ├── profiler.py
│       ├── predictor.py
│       ├── reporter.py
│       ├── decorators.py
│       ├── context.py
│       ├── exceptions.py
│       ├── config.py
│
│       ├── models/
│       │   ├── metrics.py
│       │   ├── forecast.py
│       │   └── report.py
│
│       ├── integrations/
│       │   ├── pandas.py
│       │   ├── numpy.py
│       │   ├── dask.py
│       │   └── asyncio.py
│
│       ├── exporters/
│       │   ├── json_exporter.py
│       │   ├── csv_exporter.py
│       │   └── html_exporter.py
│
│       ├── display/
│       │   ├── rich_output.py
│       │   ├── terminal.py
│       │   └── progress.py
│
│       └── utils/
│           ├── memory.py
│           ├── timing.py
│           ├── statistics.py
│           └── confidence.py
│
├── tests/
│   ├── test_forecast.py
│   ├── test_memory.py
│   ├── test_async.py
│   └── test_confidence.py
│
└── examples/
    ├── basic.py
    ├── pandas.py
    ├── numpy.py
    └── async_example.py
```

---

# Roadmap

## v1.1

* Pandas integration
* NumPy integration
* Dask integration
* CSV exports
* HTML exports

## v1.2

* Jupyter widgets
* Interactive dashboards
* Historical run comparison

## v2.0

* Machine learning forecasting engine
* GPU memory prediction
* Distributed workload prediction
* Forecast accuracy analytics

---

# Running Tests

```bash
pytest
```

Coverage:

```bash
pytest --cov=timeglance
```

---

# Contributing

Contributions are welcome.

Areas of interest:

* Forecasting algorithms
* Memory prediction models
* Visualization improvements
* Framework integrations
* Performance optimizations

---

# Philosophy

Progress bars tell you where you are.

Profilers tell you what happened.

**TimeGlance tells you what is about to happen.**

---

# License

MIT License

---

## Example

```python
from timeglance import forecast

for item in forecast(
        huge_dataset,
        sample_size=100,
        max_ram_mb=2048,
        max_time_sec=1800
):
    process(item)
```

Output:

```text
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ TimeGlance Forecast         ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ ETA           24m 18s       ┃
┃ Memory        1.2 GB        ┃
┃ Confidence    95%           ┃
┃ Throughput    521/s         ┃
┃ Risk          LOW           ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

**Forecast first. Execute smarter. 🚀**
