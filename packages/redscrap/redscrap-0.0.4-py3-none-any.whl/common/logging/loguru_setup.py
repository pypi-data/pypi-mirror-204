import sys

from common.constants.logging_constants import LoggingConstants  # type: ignore
from common.logging.utils.log_rotator import LogRotator  # type: ignore
from common.logging.utils.padding_formatter import PaddingFormatter  # type: ignore

constants = LoggingConstants()


class LoguruSetup:
    """
    A class to set up logging for scripts.

    Attributes:
        constants (LoggingConstants): an instance of LoggingConstantsNamespace class.

    Methods:
        def script_logger_config_dict: creates configuration object for scripts to setup logging.
    """

    def __init__(self) -> None:
        """
        Initializes LoggingSetup class.
        """
        super().__init__()

    @staticmethod
    def script_logger_config_dict(
            logger,
            output_directory: str,
            log_filename: str,
            level: str = constants.default_log_file_level,
            log_format: str = constants.default_log_format,
            colorize: bool = constants.default_log_colorizing,
            rotation: float = constants.default_log_rotation,
            retention: str = constants.default_log_retention,
            compression: str = constants.default_log_compression,
            delay: bool = constants.default_log_delay,
            mode: str = constants.default_log_mode,
            buffering: int = constants.default_log_buffering,
            encoding: str = constants.default_log_encoding,
            serialize: bool = constants.default_log_serialize,
            backtrace: bool = constants.default_log_backtrace,
            diagnose: bool = constants.default_log_diagnose,
            enqueue: bool = constants.default_log_enqueue,
            catch: bool = constants.default_log_catch,
            debug: bool = False,
    ):
        """
        Creates configuration object for scripts to setup logging.

        Args:
            output_directory:
            logger (Any): the logging object.
            log_filename (str): the name of the log file.
            level (str, optional): the logging level. Defaults to constants.DEFAULT_LOG_FILE_LEVEL.
            log_format (str, optional): the logging format. Defaults to constants.default_log_format.
            colorize (bool, optional): whether to colorize the logging. Defaults to constants.DEFAULT_LOG_COLORIZING.
            rotation (float, optional): the rotation size of the log file. Defaults to constants.default_log_rotation.
            retention (str, optional): the retention period of the log file. Default: constants.DEFAULT_LOG_RETENTION.
            compression (str, optional): the compression format of the log file. Default: \
             constants.DEFAULT_LOG_COMPRESSION.
            delay (bool, optional): whether to delay logging. Defaults to constants.DEFAULT_LOG_DELAY.
            mode (str, optional): the mode of the log file. Defaults to constants.DEFAULT_LOG_MODE.
            buffering (int, optional): the buffering size of the log file. Defaults to constants.DEFAULT_LOG_BUFFERING.
            encoding (str, optional): the encoding format of the log file. Defaults to constants.DEFAULT_LOG_ENCODING.
            serialize (bool, optional): whether to serialize the logging. Defaults to constants.DEFAULT_LOG_SERIALIZE.
            backtrace (bool, optional): whether to include a backtrace in the logging. Default:\
             constants.DEFAULT_LOG_BACKTRACE.
            diagnose (bool, optional): whether to diagnose the logging. Defaults to constants.DEFAULT_LOG_DIAGNOSE.
            enqueue (bool, optional): whether to enqueue the logging. Defaults to constants.DEFAULT_LOG_ENQUEUE.
            catch (bool, optional): whether to catch the logging. Defaults to constants.DEFAULT_LOG_CATCH.
            debug (bool, optional): whether to include debug messages. Defaults to False.
        """
        logger.remove()

        log_rotator = LogRotator(size=rotation, at=constants.default_log_rotation_time)
        padding_formatter = PaddingFormatter()

        sys_stdout_handler = {
            "sink": sys.stdout,
            "level": level,
            "colorize": colorize,
            "format": padding_formatter.format,
            "backtrace": backtrace,
            "diagnose": diagnose,
            "enqueue": enqueue,
            "catch": catch,
        }

        if debug:
            sys_stdout_handler["filter"] = (
                lambda record: record["level"].name == "DEBUG"
            )
        else:
            sys_stdout_handler["filter"] = lambda record: record["level"].name == "INFO"

        log_file_handler = {
            "sink": "{}/logs/{}".format(output_directory, log_filename),
            "level": level,
            "format": log_format,
            "rotation": log_rotator.should_rotate,
            "retention": retention,
            "compression": compression,
            "delay": delay,
            "mode": mode,
            "buffering": buffering,
            "encoding": encoding,
            "serialize": serialize,
            "backtrace": backtrace,
            "diagnose": diagnose,
            "enqueue": enqueue,
            "catch": catch,
        }

        config = {
            "handlers": [
                sys_stdout_handler,
                log_file_handler,
            ]
        }

        logger.level("TRACE", color="<dim>", icon=constants.rocket_symbol)
        logger.level("DEBUG", color="<dim><cyan>", icon=constants.bug_symbol)
        logger.level("INFO", color="", icon=constants.info_symbol)
        logger.level("SUCCESS", icon=constants.green_circle_symbol)
        logger.level("WARNING", color="<yellow>", icon=constants.lightning_bolt_symbol)
        logger.level("ERROR", color="<bold><red>", icon=constants.red_circle_symbol)
        logger.level("CRITICAL", color="<bold><red>", icon=constants.red_alarm_symbol)

        logger.configure(**config)
