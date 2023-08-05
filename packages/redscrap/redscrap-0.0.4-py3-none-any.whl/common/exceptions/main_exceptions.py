"""
Module responsible for holding all the custom exceptions used throughout the application
"""


class TokenErrorException(Exception):
    """
    Raises a custom exception with a message informing the user the file
    conversion process was unsuccessful.
    """

    def __init__(self, message: str):
        super().__init__(message)


class SubredditNotFoundException(Exception):
    """
    Raises a custom exception with a message informing the user the file
    conversion process was unsuccessful.
    """

    def __init__(self, message: str):
        super().__init__(message)


class UserNotFoundException(Exception):
    """
    Raises a custom exception with a message informing the user the file
    conversion process was unsuccessful.
    """

    def __init__(self, message: str):
        super().__init__(message)


class MissingRequiredParameter(Exception):
    """
    Raises a custom exception with a message informing the user about missing required parameters
    """

    def __init__(self, message: str):
        super().__init__(message)