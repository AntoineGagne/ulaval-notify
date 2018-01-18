"""This module contains useful code.

:copyright: (c) 2018 by Antoine Gagné.
:license: MIT, see LICENSE for more details.
"""

import functools


# Taken from:
# https://stackoverflow.com/q/10610824 (Wed Jan 17 15:11:46 EST 2018)
class Decorator:
    """An abstract class that simplify the creation of decorators that receives
       arguments.
    """

    def __call__(self, f):
        """Wrap the function with the `wrap` method of the implementation.

        :param f: The function to be wrapped
        :returns: The wrapped function
        """
        self.f = f
        return functools.wraps(f)(
            lambda *args, **kwargs: self.wraps(*args, **kwargs)
        )

    def wraps(self, *args, **kwrags):
        """Abstract method to decorate a function."""
        raise NotImplementedError(
            "Subclasses of Decorator must implement `wrap`"
        )


class before(Decorator):
    """Decorator that runs a function before the wrapped function.

    :param g: The function to run before the wrapped function
    """

    def __init__(self, g, *args, **kwargs):
        """Construct a `before` decorator."""
        self.g = functools.partial(g, *args, **kwargs)

    def wraps(self, *args, **kwargs):
        """Wrap the function `f`."""
        self.g()
        self.f(*args, **kwargs)


def dummy_wrap(f, *args, **kwargs):
    """Do nothing except call the function with the parameters.

    :param f: The function to be called
    """
    f(*args, **kwargs)


def run_as_daemon(f, *args, **kwargs):
    """Run the given function as a daemonized process.

    :param f: The function to run
    """
    try:
        import daemon
        with daemon.DaemonContext():
            f(*args, **kwargs)
    except ImportError:
        print('You must be on a UNIX platform to use this feature and must'
              'have installed `python-daemon`')
