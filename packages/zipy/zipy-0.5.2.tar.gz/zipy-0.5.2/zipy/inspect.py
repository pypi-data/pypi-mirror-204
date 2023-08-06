# flake8: noqa
from inspect import *  # noqa: F403


def isnormalfunc(f):
    return callable(f) and (not iscoroutinefunction(f)) and (not isasyncgenfunction(f))
