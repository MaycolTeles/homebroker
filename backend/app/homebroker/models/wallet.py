"""
Module containing the `Wallet` model.
"""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from django.db import models
from django.utils.translation import gettext_lazy as _

from account.models import User
from core.mixins import BaseModel
from core.shared import NonNegativeValueValidator
from homebroker.exceptions import WalletHasAssetsException


if TYPE_CHECKING:
    from homebroker.models import WalletAsset


class Wallet(BaseModel):
    """
    Model to store some wallet-related data.

    This model is used to store some wallet-related data.

    Attributes:
        user (`ForeignKey[User]`): The user who created the wallet.
        name (`CharField`): The name of the wallet.
        assets (`QuerySet[WalletAsset]`): The assets of the wallet.
    """

    class Meta:
        verbose_name = "Wallet"
        verbose_name_plural = "Wallets"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="wallets",
        verbose_name=_("User"),
        help_text=_("The user who created the wallet."),
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
        help_text=_("The name of the wallet."),
    )
    total_invested = models.DecimalField(
        _("Total Invested"),
        max_digits=10,
        decimal_places=2,
        default=Decimal(0.0),
        help_text=_("The total that the user invested in that wallet. Must be greater than 0.0."),
        validators=(NonNegativeValueValidator(),),
    )
    current_balance = models.DecimalField(
        _("Current Balance"),
        max_digits=10,
        decimal_places=2,
        default=Decimal(0.0),
        help_text=_("The current balance of the wallet. Must be greater than or equal to 0.0."),
        validators=(NonNegativeValueValidator(),),
    )
    assets: models.QuerySet[WalletAsset]

    @property
    def performance(self) -> Decimal:
        """
        Return the wallet's performance in %.

        The performance is calculated by subtracting the wallet's current balance
        from how much the user invested in that wallet
        and then dividing by the how much they invested.

        We multiply by 100 to have the result in percentage.

        Returns:
            `Decimal`: The calculated performance in %.
        """
        if self.total_invested == Decimal(0.0):
            return Decimal(0.0)  # Avoiding division by zero

        performance = (self.current_balance - self.total_invested) / self.total_invested
        return performance * 100  # Percent

    def add_amount_to_balance(self, amount: Decimal) -> None:
        """
        Add the received amount to the wallet balance.
        """
        self.current_balance += amount
        self.total_invested += amount
        self.save(
            update_fields=(
                "current_balance",
                "total_invested",
            )
        )

    def subtract_amount_from_balance(self, amount: Decimal) -> None:
        """
        Subtract the received amount from the wallet balance.
        """
        self.current_balance -= amount
        self.total_invested -= amount
        self.save(
            update_fields=(
                "current_balance",
                "total_invested",
            )
        )

    def delete(self, *args, **kwargs) -> None:
        """
        Delete the wallet if allowed.

        Validate that the wallet can be deleted and delete it.

        Raises:
            `WalletHasAssetsException`: If the wallet has associated assets.
        """
        if self.assets.exists():
            raise WalletHasAssetsException

        super().delete(*args, **kwargs)
