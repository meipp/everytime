import asyncio
from datetime import datetime, timedelta
from typing import Generator

millisecond = milliseconds = timedelta(milliseconds=1)
second = seconds = timedelta(seconds=1)
minute = minutes = timedelta(minutes=1)
hour = hours = timedelta(hours=1)
day = days = timedelta(days=1)
week = weeks = timedelta(weeks=1)
other = 2


def schedule_repeating_action(loop, initial_delay, delay, action) -> None:
    def repeat():
        asyncio.ensure_future(action(), loop=loop)
        loop.call_later(delay, repeat)

    loop.call_later(initial_delay, repeat)


def schedule_at(times: Generator[datetime, None, None], action, loop) -> None:
    def call_action():
        asyncio.ensure_future(action(), loop=loop)

    def repeat():
        when = None
        done = False
        try:
            when = next(times)
        except StopIteration:
            done = True

        if not done:
            delay = (when - datetime.now()).total_seconds()
            loop.call_later(delay, call_action)
            loop.call_later(delay, repeat)

    loop.call_soon(repeat)


def timeiter(start: datetime, step: timedelta) -> Generator[datetime, None, None]:
    if step <= timedelta(0):
        raise ValueError('step must be positive')

    n = start
    while True:
        yield n
        n += step


class ScheduleWithStartOffset:
    def __init__(self, initial_delay: datetime, delay: timedelta) -> None:
        self.initial_delay = initial_delay
        self.delay = delay

    def __iter__(self) -> Generator[datetime, None, None]:
        return timeiter(self.initial_delay, self.delay)

    def do(self, action, loop) -> None:
        schedule_at(iter(self), action, loop)


class ScheduleWithoutStartOffset:
    def __init__(self, step: timedelta) -> None:
        self.step = step

    def __iter__(self) -> Generator[datetime, None, None]:
        return iter(self.starting_in(timedelta(0)))

    def do(self, action, loop) -> ScheduleWithStartOffset:
        self.starting_now().do(action, loop)

    def starting_now(self) -> ScheduleWithStartOffset:
        return self.starting_in(timedelta(0))

    def starting_in(self, initial_delay: timedelta) -> ScheduleWithStartOffset:
        return self.starting_at(datetime.now() + initial_delay)

    def starting_at(self, start: datetime) -> ScheduleWithStartOffset:
        return ScheduleWithStartOffset(start, self.step)


class DayScheduleWithoutStartOffset(ScheduleWithoutStartOffset):
    def at(self, hour: float, minute: float = 0) -> ScheduleWithStartOffset:
        now = datetime.now()
        start = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if start < now:
            start += timedelta(days=1)

        return ScheduleWithStartOffset(start, self.step)


class EveryN:
    def __init__(self, n) -> None:
        self.milliseconds = ScheduleWithoutStartOffset(n * milliseconds)
        self.seconds = ScheduleWithoutStartOffset(n * seconds)
        self.minutes = ScheduleWithoutStartOffset(n * minutes)
        self.hours = ScheduleWithoutStartOffset(n * hours)
        self.days = DayScheduleWithoutStartOffset(n * days)
        self.weeks = ScheduleWithoutStartOffset(n * weeks)


class EveryOther:
    def __init__(self) -> None:
        self.millisecond = ScheduleWithoutStartOffset(other * millisecond)
        self.second = ScheduleWithoutStartOffset(other * second)
        self.minute = ScheduleWithoutStartOffset(other * minute)
        self.hour = ScheduleWithoutStartOffset(other * hour)
        self.day = DayScheduleWithoutStartOffset(other * day)
        self.week = ScheduleWithoutStartOffset(other * week)


class Every:
    def __init__(self) -> None:
        self.millisecond = ScheduleWithoutStartOffset(millisecond)
        self.second = ScheduleWithoutStartOffset(second)
        self.minute = ScheduleWithoutStartOffset(minute)
        self.hour = ScheduleWithoutStartOffset(hour)
        self.day = DayScheduleWithoutStartOffset(day)
        self.week = ScheduleWithoutStartOffset(week)

        self.other = EveryOther()

    def __call__(self, n: int) -> EveryN:
        if not isinstance(n, int):
            raise TypeError('n must be an integer')
        if n <= 0:
            raise ValueError('n must be positive')
        return EveryN(n)


every = Every()
