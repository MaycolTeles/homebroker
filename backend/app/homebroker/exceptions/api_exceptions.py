"""
Module containing all the Homebroker-related API Exceptions.
"""

from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class OrderClosedException(APIException):
    """
    Raised when trying to update an `Order` that is already closed.

    A closed order is an order that has already been executed and can't be modified anymore.
    """

    status_code = status.HTTP_409_CONFLICT
    default_detail = _("Can't update this order. The order is already closed.")
    default_code = "order_closed"


class WalletAssetHasSharesException(APIException):
    """
    Raised when trying to delete an `WalletAsset` that has shares.

    A wallet asset can't be deleted if it has shares. The shares must be sold first.
    """

    status_code = status.HTTP_409_CONFLICT
    default_detail = _("Can't delete this wallet asset. The wallet asset still has an amount of shares.")
    default_code = "wallet_asset_has_shares"


class WalletAssetHasInsufficientSharesException(APIException):
    """
    Raised when a sell order is attempted with more shares than owned.

    A sell order can't be created if the amount of shares to sell is greater than
    the amount of shares on the wallet asset.
    """

    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = _("Insufficient amount of shares to create sell order.")
    default_code = "insufficient_shares"


class WalletHasAssetsException(APIException):
    """
    Raised when trying to delete an `Wallet` that has assets.

    A wallet can't be deleted if it has assets. The assets must be removed first.
    """

    status_code = status.HTTP_409_CONFLICT
    default_detail = _("Can't delete this wallet. The wallet has assets attached to it.")
    default_code = "wallet_has_assets"
