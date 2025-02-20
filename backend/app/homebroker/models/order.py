"""
Module containing the Order model.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from account.models import User
from core.mixins import BaseModel
from homebroker.constants import ORDER_STATUS_CHOICES, ORDER_TYPE_CHOICES
from homebroker.models import Asset


class Order(BaseModel):
    """
    Model to store some order-related data.

    This model is used to store some order-related data.

    Fields:
    -----------
        * `user`: `ForeignKey[User]`
            The user who created the order.

        * `asset`: `ForeignKey[Asset]`
            The asset related to the order.

        * `shares`: `DecimalField`
            The number of shares related to the order.

        * `partial`: `IntegerField`
            The number of shares already bought.

        * `price`: `DecimalField`
            The price of the order.

        * `status`: `CharField`
            The status of the order.

        * `type`: `CharField`
            The type of the order.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name=_("User"),
        help_text=_("The user who created the order."),
    )
    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name=_("Asset"),
        help_text=_("The asset related to the order."),
    )
    shares = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Shares"),
        help_text=_("The number of shares related to the order."),
    )
    partial = models.IntegerField(
        default=0,
        verbose_name=_("Partial"),
        help_text=_("The number of shares already bought."),
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Price"),
        help_text=_("The price of the order."),
    )
    status = models.CharField(
        max_length=10,
        choices=ORDER_STATUS_CHOICES.choices,
        verbose_name=_("Status"),
        help_text=_("The status of the order."),
    )
    type = models.CharField(
        max_length=10,
        choices=ORDER_TYPE_CHOICES.choices,
        verbose_name=_("Type"),
        help_text=_("The type of the order."),
    )

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
