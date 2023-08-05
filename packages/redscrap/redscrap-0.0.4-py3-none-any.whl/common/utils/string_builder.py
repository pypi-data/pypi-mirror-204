class StringBuilder:
    """
    A class that represents a mutable sequence of characters.

    Methods:
        append_string(string: str) -> 'StringBuilder':
            Appends the given string to the current sequence.

        append_strings(*strings: str) -> 'StringBuilder':
            Appends the given strings to the current sequence.

        __str__() -> str:
            Returns a string representing the current sequence.
    """

    def __init__(self):
        self._string = []

    def append_string(self, string: str) -> "StringBuilder":
        """
        Appends the given string to the current sequence.

        Parameters:
            string (str): The string to be appended to the current sequence.

        Returns:
            (StringBuilder): The current StringBuilder object with the appended string.
        """
        self._string.append(str(string))
        return self

    def append_strings(self, *strings: str) -> "StringBuilder":
        """
        Appends the given strings to the current sequence.

        Parameters:
            strings (str): The strings to be appended to the current sequence.

        Returns:
            (StringBuilder): The current StringBuilder object with the appended strings.
        """
        for string in strings:
            self._string.append(str(string))
        return self

    def __str__(self) -> str:
        """
        Returns a string representing the current sequence.

        Returns:
            (str): A string representing the current sequence.
        """
        return "".join(self._string)
