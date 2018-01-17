import functools


# Taken from:
# https://stackoverflow.com/q/10610824 (Wed Jan 17 15:11:46 EST 2018)
class Decorator:
    def __call__(self, f):
        self.f = f
        return functools.wraps(f)(
            lambda *args, **kwargs: self.wraps(*args, **kwargs)
        )

    def wraps(self, *args, **kwrags):
        raise NotImplemented("Subclasses of Decorator must implement 'wrap'")


class before(Decorator):
    def __init__(self, g, *args, **kwargs):
        self.g = functools.partial(g, *args, **kwargs)

    def wraps(self, *args, **kwargs):
        self.g()
        self.f(*args, **kwargs)
