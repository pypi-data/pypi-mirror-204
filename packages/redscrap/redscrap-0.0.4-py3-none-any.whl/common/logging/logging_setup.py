import logging
import sys
from logging import handlers
import colorama     # type: ignore
from colorama import Fore, Back, Style

from common.constants.logging_constants import LoggingConstants      # type: ignore

logging_constants = LoggingConstants()


class FilterByModule(logging.Filter):
    """
    custom filter class called FilterByModule that inherits from logging.Filter. The filter method of this class
    is called for each log record, and it returns True if the record should be allowed through, or False if it
    should be filtered out.
    """

    def __init__(self, module_name) -> None:
        super().__init__()
        self.module_name = module_name

    def filter(self, record):
        return not record.name.startswith(self.module_name)


class LoggingSetup:
    """
    A class that sets up and configures logging for an application.

    Singleton Logger class. This class is only instantiated ONCE. It is to keep a consistent
    criteria for the logger throughout the application if need be called upon.
    It serves as the criteria for initiating logger for modules. It creates child loggers.
    It's important to note these are child loggers as any changes made to the root logger
    can be done.
    This class includes methods to set the log level of the root logger, add new loggers,
    and print logs of different levels (info, success, debug, exception, error, warning,
    and critical). It also includes methods to add and retrieve custom log level names.
    The SuccessLevel class is a custom log level used for success messages.

    Methods:
        - def get_console_handler(self):
            Defines a console handler to come out on the console
        - def get_file_handler(self):
            Defines a file handler to come out on the console.
        - def add_handlers(self, logger, handler_list: list):
            Adds handlers to the logger, checks first if handlers exist to avoid duplication
        - def get_logger(self, logger_name: str):
            Generates logger for use in the modules.
        - def set_logger(self, logger_name: str, debug_level_verbose, debug_level_non_verbose, verbose: bool):
            Sets ups a new logger
        - def set_debug_mode(self, debug_mode: bool):
            Function to set the root level logging to be debug level to be carried forward throughout
        - def get_log_level(self, level: int):
            Returns the log level legend
        - def add_level_name(self, level: int, level_name: str) -> None:
            Outputs the received message to stdout
        - def get_level_name(self, level_name: str) -> None:
            Outputs the received message to stdout
        - def silence_module_output(self, module_name: str, log_level: int) -> None:
            Filters log messages from a specific module and sets the logging level for that module
        - def print_log(self, message: str, log_type: str, verbose: bool) -> None:
            Outputs the received message to stdout.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.debug_mode = logging_constants.debug_mode_flag
            cls.formatter = logging.Formatter(logging_constants.default_logger_format)
            cls.log_file = logging_constants.log_filename

        return cls._instance

    def get_console_handler(self):
        """
        Defines a console handler to come out on the console

        Returns:
            logging handler object : the console handler
        """
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.formatter)
        console_handler.name = "consoleHandler"
        return console_handler

    def get_file_handler(self):
        """
        Defines a file handler to come out on the console.

        Returns:
            logging handler object : the console handler
        """
        file_handler = handlers.RotatingFileHandler(
            "./output/logging_logs/" + self.log_file, maxBytes=5000, backupCount=1
        )
        file_handler.setFormatter(self.formatter)
        file_handler.name = "fileHandler"
        return file_handler

    def add_handlers(self, logger, handler_list: list):
        """
        Adds handlers to the logger, checks first if handlers exist to avoid
        duplication

        Args:
            logger: Logger to check handlers'
            handler_list: list of handlers to add
        """
        existing_handler_names = []
        for existing_handler in logger.handlers:
            existing_handler_names.append(existing_handler.name)

        for new_handler in handler_list:
            if new_handler.name not in existing_handler_names:
                logger.addHandler(new_handler)

    def get_logger(self, logger_name: str):
        """
        Generates logger for use in the modules.

        Args:
            logger_name (string): name of the logger
        Returns:
            logger: returns logger for module
        """
        # Initialize the terminal for color
        colorama.init(autoreset=True)
        logger = logging.getLogger(logger_name)
        console_handler = self.get_console_handler()
        file_handler = self.get_file_handler()
        self.add_handlers(logger, [console_handler, file_handler])
        logger.propagate = False
        return logger

    def set_logger(self, logger_name: str, debug_level_verbose, debug_level_non_verbose, verbose: bool):
        """ Sets ups a new logger """
        # create a new logger with name 'example'
        logger = self.get_logger(logger_name)

        # set the logging level and formatter for the new logger
        if not verbose:
            logger.setLevel(debug_level_non_verbose)
        else:
            logger.setLevel(debug_level_verbose)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        console_handler = self.get_console_handler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    def set_debug_mode(self, debug_mode: bool):
        """
        Function to set the root level logging to be debug level to be carried forward throughout

        Args:
            debug_mode (bool): debug mode initiation if true

        Returns:

        """
        if debug_mode:
            logging.root.setLevel(logging.DEBUG)

    def get_log_level(self, level: int):
        """
        Returns the log level legend
        Values:
            CRITICAL: 50
            ERROR: 40
            WARNING: 30
            INFO: 20
            DEBUG: 10
            NOTSET: 0

        Args:
            level:

        Returns:
            Log level
        """
        return logging.getLevelName(level)

    def add_level_name(self, level: int, level_name: str) -> None:
        """
        Outputs the received message to stdout

        Args:
            level:
            level_name:

        Returns:

        """
        logging.addLevelName(level, level_name)

    def get_level_name(self, level_name: str) -> None:
        """
        Outputs the received message to stdout

        Args:
            level_name:

        Returns:

        """
        logging.getLevelName(level_name)

    def silence_module_output(self, module_name: str, log_level: int) -> None:
        """
        Filters log messages from a specific module and sets the logging level for that module.

        Args:
            module_name: str The name of the module whose log messages should be filtered.
            log_level: int The minimum logging level for messages to be output.

        Returns:
            None

        Notes:
            This method adds an instance of FilterByModule to the logger associated with the specified module,
            which filters out log messages that originate from that module. It then sets the logging level
            for that logger, which determines which log messages are output to the console or other logging destination.
        """
        logger = logging.getLogger(module_name)
        logger.addFilter(logging.Filter(__name__))
        logger.setLevel(log_level)

    def print_log(self, message: str, log_type: str, verbose: bool) -> None:
        """
        Outputs the received message to stdout.

        Args:
            message (str): The message to log.
            log_type (str): The log type to log
            verbose (bool): Whether to enable verbose logging.
        """
        if verbose:
            match log_type:
                case "debug":
                    logging.debug(message)
                case "info":
                    msg = "{} {}".format(Fore.GREEN, message)
                    logging.info(msg)
                case "warning":
                    msg = "{} {} {}".format(Fore.YELLOW, Style.BRIGHT, message)
                    logging.warning(msg)
                case "error":
                    msg = "{} {} {}".format(Fore.RED, Style.BRIGHT, message)
                    logging.error(msg)
                case "exception":
                    msg = "{} {} {}".format(Fore.CYAN, Style.BRIGHT, message)
                    logging.exception(msg)
                case "critical":
                    msg = "{} {} {} {}".format(Fore.RED, Back.YELLOW, Style.BRIGHT, message)
                    logging.critical(msg)

                case _:
                    logging.info(message)
