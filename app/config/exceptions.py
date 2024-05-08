"""
This module defines custom exception classes for the Core
"""

from sqlalchemy.exc import SQLAlchemyError


class DatabaseException(SQLAlchemyError):  # type: ignore
    """
    Database Exception class
    """

    def __init__(self, message: str, note: str | None = None):
        super().__init__(message)
        if note:
            self.add_note(note)


class ServiceException(Exception):  # type: ignore
    """
    Service Layer Exception class
    """

    def __init__(self, message: str, note: str | None = None):
        super().__init__(message)
        if note:
            self.add_note(note)
