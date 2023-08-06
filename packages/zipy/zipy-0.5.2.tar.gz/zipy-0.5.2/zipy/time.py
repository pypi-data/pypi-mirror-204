import copy
import datetime
from typing import Callable, Iterable


__all__ = ["time_range"]


def time_range(
    start: datetime.datetime, end: datetime.datetime, step: datetime.timedelta
):
    """
    :raise ValueError: raises if step is timedelta(0, 0, 0, 0, 0, 0)
    :return: an iterable object with time points within the [start, end) interval with a step of 'step'
    """
    if step == datetime.timedelta():
        raise ValueError("step can't be timedelta(0)")
    current = start
    while current < end:
        yield current
        current = current + step


def complete_timeseries(
    lst: Iterable[object],
    read_time: Callable[[object], datetime.datetime],
    write_time: Callable[[object, datetime.datetime], None],
    write_other: Callable[[object, object], None],
    step: datetime.timedelta,
):
    """
    compelete_timeseries is used to fillup missing time point in a time series

    :param lst: list of time point. Elements(time point) in the list should be in ascending order by time
    :param read_time: function to read datetime object from element of list. read_time should be like (object) -> datetime.datetime
    :param write_time: function for modifying the time of an element. write_time should be like (object, cur: datetime.datetime)
    :param write_other: function for modifying other part of an element. write_other shouble be like (object, pre: datetime.datetime)
    :param step: time interval between elements within returned list
    :raise ValueError: raises if step is datetime.timedelta(0)
    """
    start = read_time(lst[0])
    end = read_time(lst[-1])
    ret = []
    prev = lst[0]
    idx = 0
    for current in time_range(start, end, step):
        t = read_time(lst[idx])
        if t != current:
            point = copy.copy(prev)
            write_time(point, current)
            write_other(point, prev)
            ret.append(point)
            prev = point
            if t < current:
                idx += 1
        else:
            ret.append(lst[idx])
            prev = lst[idx]
            idx += 1
    if current + step == end:
        ret.append(lst[-1])
    return ret
