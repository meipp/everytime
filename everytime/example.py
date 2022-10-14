import asyncio
from everytime import *

loop = asyncio.new_event_loop()


async def greet():
    print("Hello")

every(5).seconds.do(greet, loop)
loop.run_forever()
