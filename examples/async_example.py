import asyncio

from timeglance import aforecast


async def stream():
    for item in range(5):
        await asyncio.sleep(0.01)
        yield item


async def main() -> None:
    async for item in aforecast(stream(), sample_size=2):
        print(item)


if __name__ == "__main__":
    asyncio.run(main())
