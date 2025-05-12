"""
Module containing all Order-related validators.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from account.exceptions import UserHasInsufficientBalanceException
from homebroker.constants import ORDER_STATUS_CHOICES, ORDER_TYPE_CHOICES
from homebroker.exceptions import OrderClosedException, WalletAssetHasInsufficientSharesException


if TYPE_CHECKING:
    from homebroker.models import Order


def validate_if_order_can_be_created(order: Order) -> None:
    """
    Raise an exception if the order can't be created.

    This method validates all the business logic to create an order
    based on its type

    Args:
        order (`Order`): The order object.
    """
    if order.type == ORDER_TYPE_CHOICES.BUY:
        _validate_buy_order(order)

    if order.type == ORDER_TYPE_CHOICES.SELL:
        _validate_sell_order(order)


def validate_if_order_can_be_updated(order: Order) -> None:
    """
    Raise an exception if the order can't be updated.

    This method validates all the business logic to update an order, such as:
        * Order can't be fulfilled already (i.e.: `status == CLOSED`)

    And also validates the order based on its type.

    Args:
        order (`Order`): The order object.

    Raises:
        `OrderClosedException`:
            If the order is in "CLOSED" status already.
    """
    if order.status == ORDER_STATUS_CHOICES.CLOSED:
        raise OrderClosedException

    if order.type == ORDER_TYPE_CHOICES.BUY:
        _validate_buy_order(order)

    if order.type == ORDER_TYPE_CHOICES.SELL:
        _validate_sell_order(order)


def _validate_buy_order(order: Order) -> None:
    """
    Raise an exception if the order of type `BUY` is invalid.

    This method validates all the business logic related to a `BUY` order, such as:
        * User needs to have enough balance to buy shares

    Args:
        order (`Order`): The order object.

    Raises:
        `UserHasInsufficientBalanceException`:
            If it's a "BUY" order but the user's balance is lower than the order total price.
    """
    if order.user.current_balance < order.total_price:
        raise UserHasInsufficientBalanceException


def _validate_sell_order(order: Order) -> None:
    """
    Raise an exception if the order of type `SELL` is invalid.

    This method validates all the business logic related to a `SELL` order, such as:
        * WalletAsset needs to have enough shares to sell them, etc.

    Args:
        order (`Order`): The order object.

    Raises:
        `WalletAssetHasInsufficientSharesException`:
            If it's a "SELL" order but the WalletAsset's amount of sharesis lower
                than the shares in order.
    """
    from homebroker.models import WalletAsset

    try:
        wallet_asset = WalletAsset.objects.get(wallet=order.wallet, asset=order.asset)
    except WalletAsset.DoesNotExist:
        raise WalletAssetHasInsufficientSharesException from WalletAsset.DoesNotExist

    if wallet_asset.shares < order.shares:
        raise WalletAssetHasInsufficientSharesException
