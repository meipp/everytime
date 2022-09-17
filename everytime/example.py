import asyncio
from every import *

async def do_something():
    print("Hello")

every(2 * seconds)(do_something)

loop = asyncio.get_event_loop()
loop.run_forever()
