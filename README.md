# every - Schedule asyncio coroutines

## How to use
```python
every(5 * minutes)(do_something)
every(other * day)(do_something)
every(minute).starting_at(hour=12, minute=15)(do_something)
```

## Example
```python
import asyncio
from every import *

async def do_something():
    print("Hello")

every(2 * seconds)(do_something)

loop = asyncio.get_event_loop()
loop.run_forever()
```
