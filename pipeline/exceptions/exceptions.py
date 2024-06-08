"""
A module for exceptions in the pipeline-exceptions package.
"""

from typing import Any, Union


class RateLimitExceededException(Exception):
    """Exception raised when the API rate limit is exceeded."""

    pass


class DataQualityException(Exception):
    """Exception raised for issues with the quality or format of API data."""

    pass


class ConnectionException(Exception):
    """Exception raised for network or connection issues."""

    pass


class DatabaseException(Exception):
    """Exception raised for database issues."""

    pass


class APIValidationError(Exception):
    """
    Exception raised for invalid API requests
    """

    def __init__(
        self, errors: Union[dict[str, Any], list[dict[str, Any]], str]
    ) -> None:
        self.errors = errors
        if isinstance(errors, str):
            message = errors
        elif isinstance(errors, list):
            message = "; ".join(
                [f"{err['loc']}: {err['msg']}" for err in errors]
            )
        elif isinstance(errors, dict):
            message = errors.get("message", "Unknown error")
        else:
            message = "Unexpected error format"
        super().__init__(message)


class NoAPIResponseException(Exception):
    """Exception raised when no response is received from the API."""

    pass
