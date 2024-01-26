import sys

class persistent_locals(object):
    def __init__(self, func):
        self._locals = {}
        self.func = func

    def __call__(self, *args, **kwargs):
        def tracer(frame, event, arg):
            if event=='return':
                self._locals = frame.f_locals.copy()

        sys.setprofile(tracer)
        try:
            res = self.func(*args, **kwargs)
        finally:
            sys.setprofile(None)
        return res

    def clear_locals(self):
        self._locals = {}

    @property
    def locals(self):
        return self._locals

@persistent_locals
def func():
    local1 = 1
    local2 = 2

func()
print func.locals

