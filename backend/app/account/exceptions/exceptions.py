"""
Module containing all the exceptions for the homebroker module.
"""

from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class UserAlreadyExistsException(APIException):
    """
    Raised when the `User` already exists.

    This means that the user is trying to register with an email that already exists.
    """

    status_code = status.HTTP_409_CONFLICT
    default_detail = _("User with this email already exists.")
    default_code = "user_already_exists"


class UserHasInsufficientBalanceException(APIException):
    """
    Raised when the `User` has insufficient balance.

    This means he can't buy that amount of shares.
    """

    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = _("User has insufficient balance to create buy order.")
    default_code = "user_has_insufficient_balance"
