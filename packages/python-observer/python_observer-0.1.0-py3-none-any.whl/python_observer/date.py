import time
from datetime import datetime

from humanfriendly import coerce_seconds, format_timespan


def get_current_time(time_format="%I:%M:%S %p"):
    return datetime.now().strftime(time_format)


def get_monotonic_time(should_round=True, as_seconds=False):
    multiplication_factor = 1 if as_seconds else 1000

    if should_round:
        return round(time.monotonic() * multiplication_factor)

    return time.monotonic() * multiplication_factor


def format_time(time):
    return format_timespan(coerce_seconds(time))
