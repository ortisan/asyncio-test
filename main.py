import aiohttp
import asyncio
from aiolimiter import AsyncLimiter
from datetime import datetime

# Limits with 2 RPS
limiter = AsyncLimiter(2, 1)

async def fetch(session, url):
    async with limiter:
      async with session.get(url) as response:
          print(datetime.now())
          if response.status != 200:
              response.raise_for_status()
          return await response.text()

async def fetch_all(session, urls):
    tasks = []
    for url in urls:
        task = asyncio.create_task(fetch(session, url))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results

async def main():
    urls = []
    for _ in range(10):
      urls.append("http://google.com")

    async with aiohttp.ClientSession() as session:
        htmls = await fetch_all(session, urls)
        print(htmls)

if __name__ == '__main__':
    asyncio.run(main())