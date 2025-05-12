"""
Module containing the tests for the `OrderQuerySet` queryset.
"""

from core.mixins import BaseTestCase
from homebroker.constants import ORDER_STATUS_CHOICES, ORDER_TYPE_CHOICES
from homebroker.models import Order
from homebroker.tests.mocks import MixerHomebrokerFactory


class OrderQuerySetTestCase(BaseTestCase):
    """
    Class to test the OrderQuerySet queryset.
    """

    def test_queryset_should_return_counterparty_orders(self) -> None:
        """
        Assert the queryset returns all counterparty orders.
        """
        test_share_price = 10.0
        asset = MixerHomebrokerFactory.create_asset()

        order = MixerHomebrokerFactory.create_order(
            asset=asset, status=ORDER_STATUS_CHOICES.OPEN, type=ORDER_TYPE_CHOICES.SELL, share_price=test_share_price
        )
        counterparty_order = MixerHomebrokerFactory.create_order(
            asset=asset, status=ORDER_STATUS_CHOICES.OPEN, type=ORDER_TYPE_CHOICES.BUY, share_price=test_share_price
        )

        counterparty_orders = Order.objects.counterparty_orders(order)

        self.assertIn(counterparty_order, counterparty_orders)

    def test_counterparty_orders_cant_belong_to_same_user(self) -> None:
        """
        Assert the queryset returns all counterparty orders that belong to different users.

        This means that a counterparty order can't belong to the same user as the order.
        """
        test_share_price = 10.0
        asset = MixerHomebrokerFactory.create_asset()
        user = self.create_user()

        order = MixerHomebrokerFactory.create_order(
            asset=asset,
            status=ORDER_STATUS_CHOICES.OPEN,
            type=ORDER_TYPE_CHOICES.SELL,
            share_price=test_share_price,
            user=user,
        )
        MixerHomebrokerFactory.create_order(
            asset=asset,
            status=ORDER_STATUS_CHOICES.OPEN,
            type=ORDER_TYPE_CHOICES.BUY,
            share_price=test_share_price,
            user=user,
        )

        counterparty_orders = Order.objects.counterparty_orders(order)
        self.assertEqual(counterparty_orders.count(), 0)
