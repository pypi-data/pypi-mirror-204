import datetime
import io


class LogRotator:
    """
    Custom logging formatter that applies log rotation based on time or limit.
    """
    def __init__(self, *, size: float, at: datetime.time):
        """
        Initializes a LogRotator instance.

        Args:
            size: The maximum size in bytes of the log file before it rotates.
            at: The time at which the log file should rotate.
        """
        now = datetime.datetime.now()

        self._size_limit = size
        self._time_limit = now.replace(hour=at.hour, minute=at.minute, second=at.second)

        if now >= self._time_limit:
            # The current time is already past the target time so it would rotate already.
            # Add one day to prevent an immediate rotation.
            self._time_limit += datetime.timedelta(days=1)

    def should_rotate(self, message, file: io.IOBase) -> bool:
        """
        Determines whether the log file should rotate based on the given message and file.

        Args:
            message (loguru._record.Record): A LogRecord instance representing the log message.
            file (io.IOBase): An IOBase instance representing the log file.

        Returns:
            A boolean indicating whether the log file should rotate.
        """
        file.seek(0, 2)
        if file.tell() + len(message) > self._size_limit:
            return True
        if message.record["time"].timestamp() > self._time_limit.timestamp():
            self._time_limit += datetime.timedelta(days=1)
            return True
        return False
