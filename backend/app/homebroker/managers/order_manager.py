"""
Module containing the OrderManager class.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.db import models

from homebroker.tasks import task_process_order
from homebroker.validators import order_validator


if TYPE_CHECKING:
    from homebroker.models import Order
    from homebroker.querysets import OrderQuerySet


class OrderManager(models.Manager):
    """
    Class containing all the methods to handle an Order.

    This class contains all the methods to handle an Order, such as
    `create()`, `update()` and the ones from the OrderQuerySet.
    """

    def create(self, **order_data: Any) -> Order:
        """
        Create an order.

        The process of creating an order is as follows:
            1. Validate if the order can be created;
            2. Create the order;
            3. Process (execute) the order asynchronously.

        Args:
            order_data (`dict[str, Any]`): The order data as keyword arguments.

        Returns:
            `Order`: The created order instance.
        """
        from homebroker.models import Order

        order_data["total_price"] = order_data["shares"] * order_data["share_price"]
        order = Order(**order_data)
        order_validator.validate_if_order_can_be_created(order)
        order.save()

        task_process_order.delay(order.id)

        return order

    def update(self, instance: Order, **order_data: Any) -> Order:
        """
        Update an order.

        The process of updating an order is as follows:
            1. Validate if the order can be updated;
            2. Update the order;
            3. Process (execute) the order asynchronously.

        Args:
            instance (`Order`): The order instance that will be updated.
            order_data (`dict[str, Any]`): The order data as keyword arguments.

        Returns:
            `Order`: The created order instance.
        """
        order_data["total_price"] = order_data["shares"] * order_data["share_price"]

        for field_name, value in order_data.items():
            setattr(instance, field_name, value)

        order_validator.validate_if_order_can_be_updated(instance)
        instance.save()

        task_process_order.delay(instance.id)

        return instance

    # --------- QUERYSET METHODS ---------
    def get_queryset(self) -> OrderQuerySet:
        """
        Return the OrderQuerySet instance.

        Returns:
            `OrderQuerySet`: The OrderQuerySet instance.
        """
        from homebroker.querysets import OrderQuerySet

        return OrderQuerySet(self.model, using=self._db)

    def counterparty_orders(self, order: Order) -> OrderQuerySet:
        """
        Return all counterparty orders for the given order.

        For more details, check the `counterparty_orders()` method
        from the `OrderQuerySet` class.

        Returns:
            `OrderQuerySet[Order]`: A queryset containing all counterparty orders.
        """
        return self.get_queryset().counterparty_orders(order)
