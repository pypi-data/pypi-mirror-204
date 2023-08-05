import functools
import time
from typing import Callable, Any

from loguru import logger       # type: ignore


class LoguruWrappers:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        #logger.debug("LoguruWrappers is invoked")
        return self.func(*args, **kwargs)


@LoguruWrappers
def logger_wraps(*, entry: bool = True, exit_trigger: bool = True, level: str = "DEBUG") -> Callable[..., Any]:
    """
    Decorator that logs entry and exit of a function.

    Args:
        entry: Whether to log the entry of the function.
        exit_trigger: Whether to log the exit of the function.
        level: The logging level to use for the messages.

    Returns:
        A function decorator.

    Example:
        @logger_wraps()
        def foo(x):
            return x**2
    """
    def wrapper(func: Callable[..., Any]) -> Callable[..., Any]:
        name = func.__name__

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            logger_ = logger.opt(depth=1)
            if entry:
                logger_.log(
                    level, "Entering '{}' (args={}, kwargs={})", name, args, kwargs
                )
            result = func(*args, **kwargs)
            if exit_trigger:
                logger_.log(level, "Exiting '{}' (result={})", name, result)
            return result

        return wrapped

    return wrapper


@LoguruWrappers
def timeit(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator that times the execution of a function and logs the elapsed time.

    Args:
        func: The function to decorate.

    Returns:
        The decorated function.

    Example:
        @timeit
        def foo(x):
            return x**2
    """
    def wrapped(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logger.debug("Function '{}' executed in {:f} s", func.__name__, end - start)
        return result

    return wrapped