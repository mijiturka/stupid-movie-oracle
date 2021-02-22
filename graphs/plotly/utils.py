from datetime import datetime, timedelta

def string_to_timedelta(timestamp):
    dt = datetime.strptime(timestamp, '%H:%M:%S.%f')
    return timedelta(
        hours=dt.hour,
        minutes=dt.minute,
        seconds=dt.second,
        microseconds=dt.microsecond
    )

def timedelta_to_microseconds(td):
    return td / timedelta(microseconds=1)

def string_to_microseconds(timestamp):
    return timedelta_to_microseconds(string_to_timedelta(timestamp))
