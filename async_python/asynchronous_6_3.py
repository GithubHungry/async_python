"""
Notes:
    - Write async before each function to create coroutine.
    - Write await before each blocking parts of program.
    - Wrap each coroutine in asyncio.create_task(coroutine_func()).
    - Finally create tasks with asyncio.gather(task1,task2,...).
    - Use asyncio.run(manage_func()) to create even_loop.
"""

import asyncio
from time import time

import aiohttp  # for working with http


def write_image(data):
    filename = 'file-{}.jpeg'.format(int(time() * 1000))
    with open(filename, 'wb') as file:
        file.write(data)


async def fetch_content(url, session):
    async with session.get(url, allow_redirects=True) as response:
        data = await response.read()
        write_image(data)


async def main():
    url = 'https://loremflickr.com/320/240'

    tasks = []

    async with aiohttp.ClientSession() as session:
        for i in range(10):
            task = asyncio.create_task(fetch_content(url, session))
            tasks.append(task)

        await asyncio.gather(*tasks)


if __name__ == '__main__':
    t0 = time()
    asyncio.run(main())
    print(time() - t0)
