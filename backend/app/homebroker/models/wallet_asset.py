"""
Module containing the `WalletAsset` model.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.mixins import BaseModel
from core.shared import NonNegativeValueValidator
from homebroker.exceptions import WalletAssetHasSharesException
from homebroker.models import Asset, Wallet


class WalletAsset(BaseModel):
    """
    Model to store some wallet-asset-related data.

    This model is used to store some wallet-asset-related data.

    Attributes:
        wallet (`ForeignKey[Wallet]`): The wallet to which the asset belongs.
        asset (`ForeignKey[Asset]`): The asset of the wallet.
        shares (`DecimalField`): The number of shares of the asset.
    """

    class Meta:
        verbose_name = "Wallet Asset"
        verbose_name_plural = "Wallet Assets"

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
        related_name="wallet_assets",
        verbose_name=_("Asset"),
        help_text=_("The asset of the wallet."),
    )
    shares = models.IntegerField(
        verbose_name=_("Shares"),
        help_text=_("The number of that asset shares there are in the wallet."),
        default=0,
        validators=(NonNegativeValueValidator(),),
    )

    def delete(self, *args, **kwargs) -> None:
        """
        Delete an WalletAsset instance if allowed.

        First, validates if the `WalletAsset` instance can be deleted.
        If so, then deletes it.

        Raises:
            `WalletAssetHasSharesException`: If the wallet asset has shares.
        """
        if self.shares > 0:
            raise WalletAssetHasSharesException

        super().delete(*args, **kwargs)

    def add_shares(self, shares: int) -> None:
        """
        Add shares to the wallet asset.

        This method is used to add shares to the wallet asset.

        Args:
            shares (`int`): The number of shares to be added.
        """
        self.shares += shares
        self.save(update_fields=("shares",))

    def subtract_shares(self, shares: int) -> None:
        """
        Subtract shares from the wallet asset.

        This method is used to subtract shares from the wallet asset.

        Args:
            shares (`int`): The number of shares to be subtracted.
        """
        self.shares -= shares
        self.save(update_fields=("shares",))
