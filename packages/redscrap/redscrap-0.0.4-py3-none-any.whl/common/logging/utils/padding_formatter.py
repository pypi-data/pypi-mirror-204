import loguru

from common.constants.logging_constants import LoggingConstants      # type: ignore

logging_constants = LoggingConstants()


class PaddingFormatter:
    """
    A logging formatter that adjusts padding length based on previously encountered values.

    This formatter is used to vertically align log messages by fixing the length of {name},
    {function}, and {line} fields.

    Attributes:
        padding (int): The padding length to use.
        fmt (str): The log format string to use.

    Methods:
        - format(record): Formats the log record according to the format string.
    """

    def __init__(self):
        """
        Initializes a new PaddingFormatter instance.
        """
        self.padding = 0
        self.fmt = logging_constants.padding_log_format

    def format(self, record):
        """
        Formats the specified log record.

        Args:
            record (loguru.Record): The log record to format.

        Returns:
            (str): The formatted log record string.
        """
        length = len("{name}:{function}:{line}".format(**record))
        self.padding = max(self.padding, length)
        record["extra"]["padding"] = " " * (self.padding - length)
        return self.fmt
