from datetime import datetime, timedelta
import pytz

def to_timestamp(string):
    return datetime.strptime(string, '%a %d/%m/%Y %H:%M:%S')

def scene_to_timedelta(timestamp):
    dt = datetime.strptime(timestamp, '%H:%M:%S.%f')
    return timedelta(
        hours=dt.hour,
        minutes=dt.minute,
        seconds=dt.second,
        microseconds=dt.microsecond
    )

def scene_to_timestamp(scene, start):
    return start + scene_to_timedelta(scene)

def timedelta_to_microseconds(td):
    return td / timedelta(microseconds=1)

def string_to_microseconds(timestamp):
    return timedelta_to_microseconds(string_to_timedelta(timestamp))

def localize_if_naive(dt, timezone_name):
    if dt.tzinfo is None:
        return pytz.timezone(timezone_name).localize(dt)
    return dt
