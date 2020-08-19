def assertType(context, current, expected):
    if not isinstance(current, expected):
        raise Exception(f"{context} expected to be {expected.__name__} but got {type(current).__name__}")
    return current