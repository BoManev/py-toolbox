functools import wraps

def singleton(_cls):
    _new = _cls.__new__
    singleton = None

    @wraps(_cls.__new__)
    def __new__(cls, *args, **kwargs):
        nonlocal singleton
        if singleton is None:
            singleton = _new(cls, *args, **kwargs)
        return singleton

    _cls.__new__ = __new__
    return _cls

