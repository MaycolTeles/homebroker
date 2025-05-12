"""
Module containing the OrderQuerySet class.
"""

from __future__ import annotations

from django.db.models import QuerySet

from homebroker.constants import ORDER_STATUS_CHOICES, ORDER_TYPE_CHOICES
from homebroker.models import Order


class OrderQuerySet(QuerySet[Order]):
    """
    Class containing all the methods to filter orders.
    """

    def counterparty_orders(self, order: Order) -> OrderQuerySet:
        """
        Return all counterparty orders for the given order.

        A counterparty order is an order that has the opposite type of the given order,
        but with the same asset and price.

        For example, if the given order is a "sell" order, then a counterparty order is a
        "buy" order with the same asset and price, but from a different user.

        Args:
            order (`Order`): The order to check if a counterparty order exists.

        Returns:
            `OrderQuerySet[Order]`: A queryset containing all counterparty orders, ordered by creation date.
        """
        counterparty_order_type = (
            ORDER_TYPE_CHOICES.BUY if order.type == ORDER_TYPE_CHOICES.SELL else ORDER_TYPE_CHOICES.SELL
        )

        return (
            self.filter(
                status=ORDER_STATUS_CHOICES.OPEN,
                type=counterparty_order_type,
                asset=order.asset,
                share_price=order.share_price,
            )
            .exclude(user_id=order.user.id)
            .order_by("created_at")
        )
