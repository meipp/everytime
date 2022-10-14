import asyncio
from datetime import datetime, timedelta
from typing import Generator, Iterable

millisecond = milliseconds = timedelta(milliseconds=1)
second = seconds = timedelta(seconds=1)
minute = minutes = timedelta(minutes=1)
hour = hours = timedelta(hours=1)
day = days = timedelta(days=1)
week = weeks = timedelta(weeks=1)
other = 2

monday = 0
tuesday = 1
wednesday = 2
thursday = 3
friday = 4
saturday = 5
sunday = 6


def schedule_repeating_action(loop, initial_delay, delay, action) -> None:
    def repeat():
        asyncio.ensure_future(action(), loop=loop)
        loop.call_later(delay, repeat)

    loop.call_later(initial_delay, repeat)


def schedule_at(times: Iterable[datetime], action, loop) -> None:
    iterator = iter(times)

    def call_action():
        asyncio.ensure_future(action(), loop=loop)

    def repeat():
        when = None
        done = False
        try:
            when = next(iterator)
        except StopIteration:
            done = True

        if not done:
            delay = (when - datetime.now()).total_seconds()
            loop.call_later(delay, call_action)
            loop.call_later(delay, repeat)

    loop.call_soon(repeat)


def schedule(times: Iterable[datetime], loop):
    def decorator(action):
        schedule_at(times, action, loop)
        return action
    return decorator


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
        schedule_at(self, action, loop)


class ScheduleWithoutStartOffset:
    def __init__(self, step: timedelta) -> None:
        self.step = step

    def __iter__(self) -> Generator[datetime, None, None]:
        return iter(self.starting_now())

    def do(self, action, loop) -> ScheduleWithStartOffset:
        self.starting_now().do(action, loop)

    def starting_now(self) -> ScheduleWithStartOffset:
        return self.starting_in(timedelta(0))

    def starting_in(self, initial_delay: timedelta) -> ScheduleWithStartOffset:
        return self.starting_at(datetime.now() + initial_delay)

    def starting_at(self, start: datetime) -> ScheduleWithStartOffset:
        return ScheduleWithStartOffset(start, self.step)


class DayScheduleWithoutStartOffset(ScheduleWithoutStartOffset):
    def __init__(self, step: timedelta, weekday: int = None) -> None:
        super().__init__(step)

        if weekday is not None and (weekday < 0 or weekday > 6):
            raise ValueError('weekday should be between 0 and 6')

        self.weekday = weekday

    def at(self, hour: float, minute: float = 0) -> ScheduleWithStartOffset:
        now = datetime.now()
        start = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if start < now:
            start += timedelta(days=1)

        return self.starting_at(start)

    def starting_at(self, start: datetime) -> ScheduleWithStartOffset:
        if self.weekday is not None and self.weekday != start.weekday():
            return self.starting_at(start + timedelta(days=1))

        return super().starting_at(start)


class EveryN:
    def __init__(self, n) -> None:
        if not isinstance(n, int):
            raise TypeError('n must be an integer')
        if n <= 0:
            raise ValueError('n must be positive')

        self.milliseconds = ScheduleWithoutStartOffset(n * milliseconds)
        self.seconds = ScheduleWithoutStartOffset(n * seconds)
        self.minutes = ScheduleWithoutStartOffset(n * minutes)
        self.hours = ScheduleWithoutStartOffset(n * hours)
        self.days = DayScheduleWithoutStartOffset(n * days)
        self.weeks = ScheduleWithoutStartOffset(n * weeks)

        self.mondays = DayScheduleWithoutStartOffset(n * week, weekday=monday)
        self.tuesdays = DayScheduleWithoutStartOffset(n * week, weekday=tuesday)
        self.wednesdays = DayScheduleWithoutStartOffset(n * week, weekday=wednesday)
        self.thursdays = DayScheduleWithoutStartOffset(n * week, weekday=thursday)
        self.fridays = DayScheduleWithoutStartOffset(n * week, weekday=friday)
        self.saturdays = DayScheduleWithoutStartOffset(n * week, weekday=saturday)
        self.sundays = DayScheduleWithoutStartOffset(n * week, weekday=sunday)


class EveryOther:
    def __init__(self) -> None:
        self.millisecond = ScheduleWithoutStartOffset(other * millisecond)
        self.second = ScheduleWithoutStartOffset(other * second)
        self.minute = ScheduleWithoutStartOffset(other * minute)
        self.hour = ScheduleWithoutStartOffset(other * hour)
        self.day = DayScheduleWithoutStartOffset(other * day)
        self.week = ScheduleWithoutStartOffset(other * week)

        self.monday = DayScheduleWithoutStartOffset(other * week, weekday=monday)
        self.tuesday = DayScheduleWithoutStartOffset(other * week, weekday=tuesday)
        self.wednesday = DayScheduleWithoutStartOffset(other * week, weekday=wednesday)
        self.thursday = DayScheduleWithoutStartOffset(other * week, weekday=thursday)
        self.friday = DayScheduleWithoutStartOffset(other * week, weekday=friday)
        self.saturday = DayScheduleWithoutStartOffset(other * week, weekday=saturday)
        self.sunday = DayScheduleWithoutStartOffset(other * week, weekday=sunday)


class Every:
    def __init__(self) -> None:
        self.millisecond = ScheduleWithoutStartOffset(millisecond)
        self.second = ScheduleWithoutStartOffset(second)
        self.minute = ScheduleWithoutStartOffset(minute)
        self.hour = ScheduleWithoutStartOffset(hour)
        self.day = DayScheduleWithoutStartOffset(day)
        self.week = ScheduleWithoutStartOffset(week)

        self.other = EveryOther()

        self.monday = DayScheduleWithoutStartOffset(week, weekday=monday)
        self.tuesday = DayScheduleWithoutStartOffset(week, weekday=tuesday)
        self.wednesday = DayScheduleWithoutStartOffset(week, weekday=wednesday)
        self.thursday = DayScheduleWithoutStartOffset(week, weekday=thursday)
        self.friday = DayScheduleWithoutStartOffset(week, weekday=friday)
        self.saturday = DayScheduleWithoutStartOffset(week, weekday=saturday)
        self.sunday = DayScheduleWithoutStartOffset(week, weekday=sunday)

    def __call__(self, n: int) -> EveryN:
        return EveryN(n)


every = Every()
