from typing import Dict
import logging
from colorama import Fore

colors: Dict[str, str] = {
    "DEBUG": Fore.BLUE,
    "INFO": Fore.CYAN,
    "WARNING": Fore.YELLOW,
    "ERROR": Fore.RED,
    "CRITICAL": Fore.MAGENTA,
}

class ColoredFormatter(logging.Formatter):
    """
    Custom logging formatter that applies color to log messages based on the logging level.

    Args:
        logging.Formatter: Inherited class for customizing the formatting of log messages.
    """
    def format(self, record: logging.LogRecord) -> str:
        """
        Applies color to log messages based on the logging level.

        Args:
            record: A LogRecord object representing the log message.

        Returns:
            A string with the log message and color applied.
        """
        msg = logging.Formatter.format(self, record)
        if record.levelname in colors:
            msg = colors[record.levelname] + msg + Fore.RESET
        return msg
