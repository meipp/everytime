import asyncio
from everytime import *


async def do_something():
    print("Hello")


loop = asyncio.get_event_loop()

every.other.second(do_something, loop)

loop.run_forever()
