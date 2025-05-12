"""
Module containing the `User` model.
"""

from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.mixins import BaseModel
from core.shared import MinAgeValidator, NonNegativeValueValidator


class User(AbstractUser, BaseModel):
    """
    Model to store some user-related data.
    """

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    birthdate = models.DateTimeField(
        _("Birthdate"), help_text=_("The user's birthdate."), validators=(MinAgeValidator(),)
    )
    current_balance = models.DecimalField(
        _("Current Balance"),
        max_digits=10,
        decimal_places=2,
        default=Decimal(0.0),
        help_text=_(
            "The User's current balance. Must be greater than or equal to 0. "
            "Used to determine if user can buy more shares."
        ),
        validators=(NonNegativeValueValidator(),),
    )

    REQUIRED_FIELDS = ["birthdate"]

    def add_amount_to_balance(self, amount: Decimal) -> None:
        """
        Add an amount to the user's current balance.

        Args:
            amount (`Decimal`): The amount to be added to the user's current balance.
        """
        self.current_balance += amount
        self.save(
            update_fields=("current_balance",),
        )

    def subtract_amount_from_balance(self, amount: Decimal) -> None:
        """
        Subtract an amount from the user's current balance.

        Args:
            amount (`Decimal`): The amount to be subtracted from the user's current balance.
        """
        self.current_balance -= amount
        self.save(update_fields=("current_balance",))
