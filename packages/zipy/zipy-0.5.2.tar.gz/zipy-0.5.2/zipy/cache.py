import time
from zipy import inspect


__all__ = ["cache"]


def _make_key(args: tuple, kwargs: dict):
    key = args
    for k in sorted(kwargs):
        key += (k, kwargs[k], type(kwargs[k]))
    key += tuple(type(v) for v in args)
    return hash(key)


def cache(*, ttl: float = 0):
    """
    Cache result of function. function can be either normal ,coroutine or asyncgen function

    :param ttl: time to live in seconds. ttl <= 0 means forever
    :raise ValueError: raises if func is neither normal, coroutine nor asyncgen function
    :return: decorator
    """

    def decorator(func):
        # structure: {"revoke_sig": [result, birthday]}
        cached = {}

        if inspect.iscoroutinefunction(func):

            async def wrapper(*args, **kwargs):
                nonlocal cached
                key = _make_key(args, kwargs)
                result, birthday = cached.get(key, [None, 0])

                isforever = ttl <= 0
                isexpired = time.time() - birthday >= ttl
                if (result is not None) and (isforever or (not isexpired)):
                    return result
                else:
                    result = await func(*args, **kwargs)
                    cached[key] = [result, time.time()]
                    return result

            return wrapper
        elif inspect.isnormalfunc(func):

            def wrapper(*args, **kwargs):
                nonlocal cached
                key = _make_key(args, kwargs)
                result, birthday = cached.get(key, [None, 0])

                isforever = ttl <= 0
                isexpired = time.time() - birthday >= ttl
                if (result is not None) and (isforever or (not isexpired)):
                    return result
                else:
                    result = func(*args, **kwargs)
                    cached[key] = [result, time.time()]
                    return result

            return wrapper
        elif inspect.isasyncgenfunction(func):

            async def wrapper(*args, **kwargs):
                nonlocal cached
                key = _make_key(args, kwargs)
                result, birthday = cached.get(key, [None, 0])

                isforever = ttl <= 0
                isexpired = time.time() - birthday >= ttl
                if (result is not None) and (isforever or (not isexpired)):
                    for ele in result:
                        yield ele
                else:
                    result = []
                    async for ele in func(*args, **kwargs):
                        result.append(ele)
                        yield ele
                    cached[key] = [result, time.time()]

            return wrapper
        else:
            raise ValueError(
                f"{func} is neither normal, coroutine nor asyncgen function"
            )

    return decorator
