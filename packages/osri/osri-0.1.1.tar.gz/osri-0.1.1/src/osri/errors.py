"""
This module contains error handling related code.
"""

class OSRIError(Exception):
    """
    Base project error class.

    All specialized errors should inherit this class.
    """
    def __init__(self, message: str, code: int = 1) -> None:
        """
        Create a new error instance with a message and a code.

        Code defaults to `1`.
        """
        super(OSRIError, self).__init__(message)

        self.message = message
        self.code = code

    def __str__(self) -> str:
        """
        Return the error string representation as `$self.code $self.message`.
        """
        return f'[{self.code}] {self.message}'
