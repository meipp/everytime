# everytime - Schedule asyncio coroutines

## TLDR
```python
@every.other.wednesday.at(hour=12)
async def do_something():
    ...
```

## Full Example
```python
from everytime import every
import everytime

@every(5).seconds
async def greet():
    print("Hello")

everytime.run_forever()
```

## How to schedule coroutines

### everytime expressions as decorators
All everytime expressions can be used as function decorators.
```python
@every(5).seconds
async def greet():
    print("Hello")
```

### @schedule
Aternatively you can wrap the everytime expression into a call to `@schedule`.
```python
@schedule(every(5).seconds)
async def greet():
    print("Hello")
```
This allows you to pass custom datetime iterables to `@schedule` (see [Schedule custom times](#schedule-custom-times)).

<a id="schedule-custom-times"/>

#### Schedule custom times
`@schedule` accepts datetime iterables. The following schedules work:
```python
@schedule([datetime.fromisoformat('2022-11-01T12:00:00'), datetime.fromisoformat('2023-01-01T12:00:00')])

@schedule(itertools.islice(every.day, 5))

@schedule(map(lambda _: datetime.now() + timedelta(seconds=1), sys.stdin))
```

### do()
If you prefer to keep your function definitions and scheduling rules separate, use the `do`-function.
```python
async def greet():
    print("Hello")

every(5).seconds.do(greet)
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

## Event Loops
everytime uses `asyncio` and schedules coroutines on an event loop.

### Default Behavior
By default, all coroutines are scheduled on the same event loop. After all schedules are set, the loop must be invoked with `everytime.run_forever()`
```python
@schedule(every.second)
async def greet():
    print("Hello")

everytime.run_forever()
```


### Async Environment
If called in an async environment (i.e. there is already an event loop running), coroutines are scheduled on `asyncio.get_running_loop()`.

```python
async def main():
    @schedule(every.second)
    async def greet():
        print("Hello")

    await asyncio.sleep(10)

asyncio.run(main())
```

Note, that the scheduling only works while the loop is running. In this case, `greet` will only be called every second, while `main` is still running.

### Custom Event Loops
You can schedule your coroutines to run on a custom event loop by passing an optional argument `loop` to`@schedule` or `do()`.

```python
l = asyncio.new_event_loop()

@schedule(every.second, loop=l)
async def greet():
    print("Hello")

l.run_forever()
```

```python
l = asyncio.new_event_loop()

async def greet():
    print("Hello")

every.second.do(greet, loop=l)
l.run_forever()
```
