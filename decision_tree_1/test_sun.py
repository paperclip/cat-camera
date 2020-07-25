#!/bin/env python


try:
    from . import sun
except ImportError:
    import sun

import pytz
import datetime

SUN = sun.sun(lat=51.6080, long=-1.2448)
TIMEZONE = pytz.timezone("Europe/London")


def get_datetime(record):
    return TIMEZONE.localize(
            datetime.datetime(
            record['year'],
            record['month'],
            record['day_of_month'],
            record['hour'],
            record['minute'],
            record['second'])
        )


def get_sunrise(record):
    record_datetime = get_datetime(record)
    sunrise_time = SUN.sunrise(record_datetime)
    sunrise_datetime = datetime.datetime.combine(record_datetime, sunrise_time)
    ret = TIMEZONE.localize(sunrise_datetime)
    return ret


def get_sunset(record):
    record_datetime = get_datetime(record)
    sunset_time = SUN.sunset(record_datetime)
    sunset_datetime = datetime.datetime.combine(
        record_datetime.date(), sunset_time)
    return TIMEZONE.localize(sunset_datetime)

record = {
    'year': 2020,
    'month': 1,
    'day_of_month': 21,
    'hour': 18,
    'minute': 36,
    'second': 00
}
print(get_sunrise(record), get_sunset(record))

record['month'] = 6
print(get_sunrise(record), get_sunset(record))

record['month'] = 7
print(get_sunrise(record), get_sunset(record))

record['day_of_month'] = 25
sunrise = get_sunrise(record)
print(sunrise, get_sunset(record))
assert sunrise.hour == 5

record['month'] = 8
record['day_of_month'] = 1
print(get_sunrise(record), get_sunset(record))

record['day_of_month'] = 21
record['month'] = 12
print(get_sunrise(record), get_sunset(record))
