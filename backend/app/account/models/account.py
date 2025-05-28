"""
Module containing the `Account` model.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from account.models.user import User
from core.mixins import BaseModel


class Account(BaseModel):
    """
    Model to store some account-related data.
    """

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="accounts",
        verbose_name=_("User"),
        help_text=_("The User associated with the account."),
    )

    name = models.CharField(
        max_length=20,
        help_text=_("The account name."),
    )

    bank = models.CharField(
        max_length=10,
        help_text=_("The bank code associated with the account."),
    )

    agency = models.CharField(
        max_length=10,
        help_text=_("The agency number associated with the account."),
    )

    account_number = models.CharField(
        max_length=20,
        help_text=_("The account number associated with the account."),
    )
