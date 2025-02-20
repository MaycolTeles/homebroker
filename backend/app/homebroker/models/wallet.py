"""
Module containing the Wallet model.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models
from django.utils.translation import gettext_lazy as _

from account.models import User
from core.mixins import BaseModel


if TYPE_CHECKING:
    from homebroker.models import WalletAsset


class Wallet(BaseModel):
    """
    Model to store some wallet-related data.

    This model is used to store some wallet-related data.

    Fields:
    -----------
        * `user`: `ForeignKey[User]`
            The user who created the wallet.

        * `name`: `CharField`
            The name of the wallet.

        * `assets`: `QuerySet[WalletAsset]`
            The assets of the wallet.
    """

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
    assets: models.QuerySet[WalletAsset]

    class Meta:
        verbose_name = "Wallet"
        verbose_name_plural = "Wallets"
