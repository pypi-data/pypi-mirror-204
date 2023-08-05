import logging
from typing import Callable


class LoggingWrappers:
    """
    A class that provides logging decorators to log function call arguments and return values.

    Attributes:

    Methods:
        logging_decorator: A decorator that logs function call arguments and return values.
    """

    def __init__(self) -> None:
        super().__init__()

    def logging_decorator(self, name: str) -> Callable:
        """
        A decorator that logs function call arguments and return values.

        Args:
            name: The name of the logger.

        Returns:
            A function that logs function call arguments and return values.
        """
        logger = logging.getLogger(name)

        def _decor(fn):
            function_name = fn.__name__

            def _fn(*args, **kwargs):
                ret = fn(*args, **kwargs)
                argstr = [str(x) for x in args]
                argstr += [key + "=" + str(val) for key, val in kwargs.items()]
                logger.debug("%s(%s) -> %s", function_name, ", ".join(argstr), ret)
                return ret

            return _fn

        return _decor
