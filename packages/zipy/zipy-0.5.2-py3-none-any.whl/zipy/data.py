def dict_get(d, *keys, default=None) -> object:
    """
    access nested dict recursively without KeyError

    Example:
    d = {"a": {"b": 123}}
    dict_get(d, "a", "b")
    >> 123
    dict_get(d, "a", "b", "c")
    >> None

    :param d: dict
    :param default: if there is no specific key in specific depth of the dict, return default
    :param keys: keys are used to access nested dict orderly
    :retrun: object
    """
    for k in keys:
        try:
            d = d[k]
        except (TypeError, KeyError):
            d = default
            break
    return d
