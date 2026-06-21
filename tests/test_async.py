import asyncio
from pathlib import Path

from timeglance import aforecast


async def _stream(count: int):
    for item in range(count):
        await asyncio.sleep(0)
        yield item


def test_aforecast_iterates_async_values():
    async def run():
        seen = []

        async for item in aforecast(_stream(4), sample_size=2):
            seen.append(item)

        return seen

    assert asyncio.run(run()) == [0, 1, 2, 3]


def test_aforecast_exports_report(tmp_path: Path):
    async def run():
        async for _ in aforecast(_stream(2), export=str(target)):
            pass

    target = tmp_path / "async-report.csv"
    asyncio.run(run())

    assert target.exists()
    assert "completed" in target.read_text(encoding="utf-8")
