"""
Module containing the WalletAsset model.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.mixins import BaseModel
from homebroker.models import Asset, Wallet


class WalletAsset(BaseModel):
    """
    Model to store some wallet-asset-related data.

    This model is used to store some wallet-asset-related data.

    Fields:
    -----------
        * `wallet`: `ForeignKey[Wallet]`
            The wallet to which the asset belongs.

        * `asset`: `ForeignKey[Asset]`
            The asset of the wallet.

        * `shares`: `DecimalField`
            The number of shares of the asset.
    """

    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name="assets",
        verbose_name=_("Wallet"),
        help_text=_("The wallet to which the asset belongs."),
    )
    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name="wallet",
        verbose_name=_("Asset"),
        help_text=_("The asset of the wallet."),
    )
    shares = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Shares"),
        help_text=_("The number of shares of the asset."),
    )

    class Meta:
        verbose_name = "WalletAsset"
        verbose_name_plural = "WalletAssets"
