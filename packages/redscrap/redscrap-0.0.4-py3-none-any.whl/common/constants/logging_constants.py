from datetime import time

import loguru


class LoggingConstants:
    """
    A class that contains logging constants used for configuring logging settings. The properties of this class
    represent the logging levels and their corresponding severity levels, as well as various symbols and log formats
    used in the logging process.

    Methods:
    log_filename (str): The name of the log file to be used for logging.
    trace_level (str): The logging level for trace messages.
    trace_severity_level (int): The severity level for trace messages.
    debug_level (str): The logging level for debug messages.
    debug_severity_level (int): The severity level for debug messages.
    info_level (str): The logging level for info messages.
    info_severity_level (int): The severity level for info messages.
    success_level (str): The logging level for success messages.
    success_severity_level (int): The severity level for success messages.
    warning_level (str): The logging level for warning messages.
    warning_severity_level (int): The severity level for warning messages.
    error_level (str): The logging level for error messages.
    error_severity_level (int): The severity level for error messages.
    critical_level (str): The logging level for critical messages.
    critical_severity_level (int): The severity level for critical messages.
    bug_symbol (str): The symbol used to represent a bug.
    robot_symbol (str): The symbol used to represent a robot.
    rocket_symbol (str): The symbol used to represent a rocket.
    red_alarm_symbol (str): The symbol used to represent a red alarm.
    red_circle_symbol (str): The symbol used to represent a red circle.
    green_circle_symbol (str): The symbol used to represent a green circle.
    warning_symbol (str): The symbol used to represent a warning.
    lightning_bolt_symbol (str): The lightning bolt symbol as a string: "⚡".
    skull_symbol (str): The skull symbol as a string: "☠️".
    check_mark_symbol (str): The check mark symbol as a string: "✔️".
    cross_symbol (str): The cross symbol as a string: "❌".
    info_symbol (str): The information symbol as a string: "🛈 ".
    default_log_format (str): The default log format as a string, which consists of a time stamp, log level, file name,
    function name, line number, and log message.
    default_log_format2 (str): An alternative default log format as a string, which consists of a time stamp, log level,
    file name, function name, line number, and log message.
    padding_log_format (str): A padded log format as a string, which consists of a time stamp, log level, file name,
    function name, line number, log message, and exception details.
    """

    @property
    def log_filename(self):
        """
        The name of the log file to be used for logging.

        Returns:
             (str): the name of the log file to be used for logging.
        """
        return "redscrap.log"

    @property
    def trace_level(self):
        """
        The logging level for trace messages.

        Returns:
             (str): the logging level for trace messages.
        """
        return "TRACE"

    @property
    def trace_severity_level(self):
        """
        The severity level for trace messages.

        Returns:
             (int): the severity level for trace messages.
        """
        return 5

    @property
    def debug_level(self):
        """
        The logging level for debug messages.

        Returns:
             (str): the logging level for debug messages.
        """
        return "DEBUG"

    @property
    def debug_severity_level(self):
        """
        The severity level for debug messages.

        Returns:
             (int): the severity level for debug messages.
        """
        return 10

    @property
    def info_level(self):
        """
        The logging level for info messages.

        Returns:
             (str): the logging level for info messages.
        """
        return "INFO"

    @property
    def info_severity_level(self):
        """
        The severity level for info messages.

        Returns:
             (int): the severity level for info messages
        """
        return 20

    @property
    def success_level(self):
        """
        The logging level for success messages.

        Returns:
             (str): the logging level for success messages.
        """
        return "SUCCESS"

    @property
    def success_severity_level(self):
        """
        The severity level for success messages.

        Returns:
             (int): the severity level for success messages.
        """
        return 25

    @property
    def warning_level(self):
        """
        The logging level for warning messages.

        Returns:
             (str): the logging level for warning messages.
        """
        return "WARNING"

    @property
    def warning_severity_level(self):
        """
        The severity level for warning messages.

        Returns:
             (int): the severity level for warning messages.
        """
        return 30

    @property
    def error_level(self):
        """
        The logging level for error messages.

        Returns:
             (str): the logging level for error messages.
        """
        return "ERROR"

    @property
    def error_severity_level(self):
        """
        The severity level for error messages.

        Returns:
             (int): the severity level for error messages.
        """
        return 40

    @property
    def critical_level(self):
        """
        The logging level for critical messages.

        Returns:
             (str): the logging level for critical messages.
        """
        return "CRITICAL"

    @property
    def critical_severity_level(self):
        """
        The severity level for critical messages.

        Returns:
             (int): the severity level for critical messages.
        """
        return 50

    @property
    def bug_symbol(self):
        """
        The bug symbol as a string: "🐞".

        Returns:
             (str): the bug symbol as a string: "🐞".
        """
        return "🐞"

    @property
    def robot_symbol(self):
        """
        The robot symbol as a string: "🤖".

        Returns:
             (str): the robot symbol as a string: "🤖".
        """
        return "🤖"

    @property
    def rocket_symbol(self):
        """
        The rocket symbol as a string: "🚀".

        Returns:
             (str): the rocket symbol as a string: "🚀".
        """
        return "🚀"

    @property
    def red_alarm_symbol(self):
        """
        The red alarm symbol as a string: "🚨".

        Returns:
             (str):  the red alarm symbol as a string: "🚨".
        """
        return "🚨"

    @property
    def red_circle_symbol(self):
        """
        The red circle symbol as a string: "🔴".

        Returns:
             (str): the red circle symbol as a string: "🔴"
        """
        return "🔴"

    @property
    def green_circle_symbol(self):
        """
        The green circle symbol as a string: "🟢".

        Returns:
             (str): the green circle symbol as a string: "🟢"
        """
        return "🟢"

    @property
    def warning_symbol(self):
        """
        The warning symbol as a string: "⚠️".

        Returns:
             (str): the  warning symbol as a string: "⚠️"
        """
        return "⚠️"

    @property
    def lightning_bolt_symbol(self):
        """
        The lightning bolt symbol as a string: "⚡".

        Returns:
             (str):
        """
        return "⚡"

    @property
    def skull_symbol(self):
        """
        The skull symbol as a string: "☠️"

        Returns:
             (str): the skull symbol as a string: "☠️".
        """
        return "☠️"

    @property
    def check_mark_symbol(self):
        """
        The check mark symbol as a string: "✔️".

        Returns:
             (str): the check mark symbol as a string: "✔️"
        """
        return "✔️"

    @property
    def cross_symbol(self):
        """
        The cross symbol as a string: "❌"

        Returns:
             (str): the cross symbol as a string: "❌".
        """
        return "❌"

    @property
    def info_symbol(self):
        """
        The information symbol as a string: "🛈 "

        Returns:
             (str): the information symbol as a string: "🛈 ".
        """
        return "🛈 "

    @property
    def default_log_format(self):
        """
        The default log format as a string, which consists of a time stamp, log level, file name,
        function name, line number, and log message.

        Returns:
             (str): the default log format as a string, which consists of a time stamp, log level, file name,
        function name, line number, and log message.
        """
        log_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level.icon}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>"
            " - <level>{message}</level>"
        )
        return log_format

    @property
    def default_log_format2(self):
        """
        An alternative default log format as a string, which consists of a time stamp, log level, file name,
        function name, line number, and log message.

        Returns:
             (str): an alternative default log format as a string
        """
        return (
            "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {level.icon}"
            "| {name}:{function}:{line} | {message}"
        )

    @property
    def padding_log_format(self):
        """
        A padded log format as a string, which consists of a time stamp, log level, file name, function name,
        line number, log message, and exception details.

        Returns:
             (str): a  padded log format as a string
        """
        log_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level.icon}</level> <level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}{extra[padding]}</cyan> - "
            "<level>{message}\n{exception}</level>"
        )
        return log_format

    @property
    def default_logger_format(self):
        """
        The default logger format as a string, which consists of a time stamp, log level, logger name, and
        log message.

         Returns:
             (str): the default logger format as a string
        """
        return "%(asctime)s - %(levelname)-4s - %(name)-s - %(message)s"

    @property
    def default_logger_date_format(self):
        """
        The default logger date format as a string, which consists of the day, month, year, hour, minute, and
        second.

        Returns:
             (str): the default logger date format as a string
        """
        return "%d-%b-%Y %H:%M:%S"

    @property
    def debug_mode_flag(self):
        """
        A boolean value indicating whether debug mode is enabled or not.

        Returns:
             (bool): boolean value indicating whether debug mode is enabled or not
        """
        return True

    @property
    def default_log_rotation_time(self):
        """
        A time object representing the default log rotation time, which is midnight (0 hours, 0 minutes,
        0 seconds).

         Returns:
             (time):  a time object representing the default log rotation time
        """
        datetime = time(0, 0, 0)
        return datetime

    def default_log_file_level(self):
        """
        The default logger date format as a string, which consists of the day, month, year, hour, minute, and
        second.

        Returns:
            (str):
        """

        return loguru.logger.level("20").name

    @property
    def default_log_stfout_level(self):
        """
        A string representing the default logging level for standard output.

        Returns:
             (str):
        """
        return "INFO"

    @property
    def default_log_stdout_level(self):
        """
        A string representing the default logging level for standard output.

        Returns:
             (str):
        """
        return "INFO"

    @property
    def default_log_colorizing(self):
        """
        A boolean representing whether log output should be colorized by default.

        Returns:
             (bool): a boolean representing whether log output should be colorized by default
        """
        return True

    @property
    def default_log_rotation(self):
        """
        A float representing the default maximum size of the log file before it is rotated.

        Returns:
             (float): a float representing the default maximum size of the log file before it is rotated
        """
        return 5e8

    @property
    def default_log_retention(self):
        """
        A string representing the default retention period for log files.

        Returns:
             (str): a string representing the default retention period for log files
        """
        return "10 days"

    @property
    def default_log_compression(self):
        """
        A string representing the default compression type for log files.

        Returns:
             (str): a string representing the default compression type for log files
        """
        return "zip"

    @property
    def default_log_delay(self):
        """
        A boolean representing whether log messages should be written immediately or with a delay.

        Returns:
             (bool): a boolean representing whether log messages should be written immediately or with a delay
        """
        return False

    @property
    def default_log_mode(self):
        """
        A string representing the default mode for opening log files.

        Returns:
             (str): a string representing the default mode for opening log files
        """
        return "a"

    @property
    def default_log_buffering(self):
        """
        An integer representing the default buffering value for log files.

        Returns:
             (int): an integer representing the default buffering value for log files
        """
        return 1

    @property
    def default_log_encoding(self):
        """
        A string representing the default character encoding for log files.

        Returns:
             (str): a string representing the default character encoding for log files
        """
        return "utf8"

    @property
    def default_log_serialize(self):
        """
        A boolean representing whether log messages should be serialized by default.

        Returns:
             (bool): a boolean representing whether log messages should be serialized by default
        """
        return True

    @property
    def default_log_backtrace(self):
        """
        A boolean representing whether a backtrace should be included in log messages by default.

        Returns:
             (bool):  a boolean representing whether a backtrace should be included in log messages by default
        """
        return False

    @property
    def default_log_diagnose(self):
        """
        A boolean representing whether diagnosis information should be included in log messages by default.

        Returns:
             (bool): a boolean representing whether diagnosis information should be included in log messages by default
        """
        return False

    @property
    def default_log_enqueue(self):
        """
        A boolean representing whether log messages should be enqueued for writing by default.

        Returns:
             (bool): a boolean representing whether log messages should be enqueued for writing by default
        """
        return False

    @property
    def default_log_catch(self):
        """
        A boolean representing whether exceptions should be caught during log writing by default.

        Returns:
             (bool):  a boolean representing whether exceptions should be caught during log writing by default
        """
        return False
