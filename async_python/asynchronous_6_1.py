"""
Asyncio framework.
Notes:
    - Coroutines creates by using 'async def fun_1'  -> create coroutine-gen from an function.
    - await equal to yield from.
    - Never use sleep(blocking function) -> use asyncio.sleep() instead of.
    - Create task from coroutines using: task1=asyncio.create_task(coroutine_function_1())
    - Collect all tasks: await asyncio.gather(task1,task2,...)
    - Create and run event_loop using: asyncio.run(manage_main_function())
Results:
    -
"""
import asyncio


# @asyncio.coroutine  # create coroutine from function python3.4 -> python3.5
async def print_nums():
    num = 1
    while True:
        print(num)
        num += 1
        await asyncio.sleep(0.1)


# @asyncio.coroutine  # create coroutine from function (python3.4)
async def print_time():  # python 3.5
    count = 0
    while True:
        if count % 3 == 0:
            print('{} seconds have passed.'.format(count))
        count += 1
        await asyncio.sleep(1)  # yield from ..  -> await (3.4->3.5)


# @asyncio.coroutine  # create coroutine from function
async def main():  # event loop?  -> func which manage tasks
    # task1 = asyncio.ensure_future(print_nums())  # Create tasks, () must have in generators!
    task1 = asyncio.create_task(print_nums())  # ensure_future -> create_task
    task2 = asyncio.create_task(print_time())  # All tasks passed to the tasks queue

    await asyncio.gather(task1, task2)  # yield from ..  -> await (3.4->3.5)


if __name__ == '__main__':
    # loop = asyncio.get_event_loop()  # Create async_loop
    # loop.run_until_complete(main())  # Start async_loop (pass coroutine which create tasks (kind of delegator???))
    # loop.close()
    asyncio.run(main())  # 3 rows = asyncio.run(main()) python3.6
