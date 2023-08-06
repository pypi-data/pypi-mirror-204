import datetime
import logging
import time


def get_readable_time():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y.%m.%d_%H.%M.%S')


def mils_to_datetime(mls):
    return datetime.datetime.fromtimestamp(mls / 1000).strftime('%Y.%m.%d_%H.%M.%S')


def interval_to_millisecs(interval_str):
    assert len(interval_str) <= 3, "must be in {1m 3m 5m 15m 30m 1h 2h 4h 6h 8h 12h 1d 3d 1w 1M}"
    unit = interval_str[-1:]
    num = int(interval_str[:-1])
    if unit == "m":
        return 60 * 1000 * num
    if unit == "h":
        return 60 * 60 * 1000 * num
    if unit == "d":
        return 24 * 60 * 60 * 1000 * num
    if unit == "w":
        return 7 * 24 * 60 * 60 * 1000 * num
    if unit == "M":
        return 30 * 7 * 24 * 60 * 60 * 1000 * num
    logging.warning("Invalid interval, use default interval 3m")
    return 60 * 1000 * 3
