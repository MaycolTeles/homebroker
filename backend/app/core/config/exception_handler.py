"""
Module containing the `custom_exception_handler` function.
"""

from typing import Any

from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc: APIException, context: dict[str, Any]) -> Response:
    """
    Add some details to API exceptions.

    This function adds some metadata to the response when an API exception occurs.

    Args:
        exc (`APIException`): The API exception.
        context (`dict[str, Any]`): The API exception context (used by DRF).

    Returns:
        `Response`: API Response with the new metadata fields.
    """
    response = exception_handler(exc, context)

    # Only modify response for DRF APIExceptions
    if isinstance(exc, APIException):
        response.data = {
            "detail": exc.detail,
            "code": exc.default_code,
        }

    return response  # type: ignore
