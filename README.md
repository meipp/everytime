# everytime - Schedule asyncio coroutines

## TLDR
```python
@schedule(every.other.wednesday.at(hour=12), loop)
async def do_something():
    ...
```
to schedule `do_something()` every second Wednesday at 12:00 on the `asyncio.EventLoop` called `loop`. `loop` has to be running for that.

## Full Example
```python
import asyncio
from everytime import *

loop = asyncio.new_event_loop()

async def greet():
    print("Hello")

every(5).seconds.do(greet, loop)
loop.run_forever()
```

## Schedule with do()
You can schedule actions with the `do` function.
```python
async def greet():
    print("Hello")

every(5).seconds.do(greet, loop)
```

## Schedule with decorators
If you prefer, you can decorate your action with an everytime expression.
```python
@schedule(every(5).seconds, loop)
async def greet():
    print("Hello")
```

## Schedule custom times
`@schedule` accepts datetime iterables. The following schedules work:
```python
@schedule([datetime.fromisoformat('2022-11-01T12:00:00'), datetime.fromisoformat('2023-01-01T12:00:00')], loop)

@schedule(itertools.islice(every.day, 5), loop)

@schedule(map(lambda _: datetime.now() + timedelta(seconds=1), sys.stdin), loop)
```

## Supported Expressions

### Quantification
Every time unit can be quantified by `every`, `every.other` or `every(n)`:
- `every.second`
- `every.other.second`
- `every(5).seconds`

### Supported time units
The supported time units are
- `millisecond`
- `second`
- `minute`
- `hour`
- `day`
- `week`

### Weekdays
Also, weekdays `monday` through `sunday` are supported. `every.wednesday` starts on the next Wednesday. If today is a Wednesday, `every.wednesday` starts today.

### Specific time of the day
`day` and the weekdays can be scheduled for a specific time of the day:
```python
every.day.at(hour=12, minute=15)
```
(Note that `hour` is 24-hour based)
