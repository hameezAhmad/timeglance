"""Practical TimeGlance example: monitor a small batch ETL workflow.

Run from the repository root with:

    python examples/practical_batch_etl.py

In a notebook, copy `run_batch_etl()` and call it directly.
"""

from __future__ import annotations

import random
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from timeglance import forecast
from timeglance.display import render_forecast


def load_customer_ids(total: int = 250) -> list[int]:
    """Pretend these IDs came from a database query."""

    return list(range(1, total + 1))


def fetch_customer_record(customer_id: int) -> dict[str, object]:
    """Pretend this is an API call with variable network latency."""

    time.sleep(random.uniform(0.001, 0.006))
    return {
        "customer_id": customer_id,
        "orders": random.randint(0, 20),
        "account_age_days": random.randint(1, 2000),
    }


def enrich_record(record: dict[str, object]) -> dict[str, object]:
    """Add a simple derived field like a real ETL transform would."""

    orders = int(record["orders"])
    account_age_days = int(record["account_age_days"])
    record["segment"] = "loyal" if orders >= 10 and account_age_days > 365 else "standard"
    return record


def save_records(records: list[dict[str, object]], output_path: Path) -> None:
    """Write a tiny CSV without pulling in extra dependencies."""

    rows = ["customer_id,orders,account_age_days,segment"]
    for record in records:
        rows.append(
            f"{record['customer_id']},{record['orders']},"
            f"{record['account_age_days']},{record['segment']}"
        )
    output_path.write_text("\n".join(rows), encoding="utf-8")


def run_batch_etl() -> None:
    output_dir = Path("example-output")
    output_dir.mkdir(exist_ok=True)

    customer_ids = load_customer_ids()
    monitored_ids = forecast(
        customer_ids,
        sample_size=20,
        update_every=50,
        max_time_sec=3,
        max_ram_mb=256,
        export=str(output_dir / "timeglance-report.json"),
    )

    processed: list[dict[str, object]] = []
    last_reported_checkpoint = 0
    print("Starting customer ETL job...")

    for customer_id in monitored_ids:
        record = fetch_customer_record(customer_id)
        processed.append(enrich_record(record))

        latest = monitored_ids.latest
        if latest and latest.completed % 50 == 0 and latest.completed != last_reported_checkpoint:
            last_reported_checkpoint = latest.completed
            print()
            print(render_forecast(latest))

    save_records(processed, output_dir / "customers.csv")

    print()
    print("Finished customer ETL job.")
    print(f"Processed records: {len(processed)}")
    print(f"Data output: {output_dir / 'customers.csv'}")
    print(f"Forecast report: {output_dir / 'timeglance-report.json'}")

    if monitored_ids.latest:
        print()
        print("Final usability summary:")
        print(render_forecast(monitored_ids.latest))


if __name__ == "__main__":
    run_batch_etl()
