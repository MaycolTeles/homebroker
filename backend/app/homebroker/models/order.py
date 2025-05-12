"""
Module containing the `Order` model.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from account.models import User
from core.mixins import BaseModel
from homebroker.constants import ORDER_STATUS_CHOICES, ORDER_TYPE_CHOICES
from homebroker.managers import OrderManager
from homebroker.models.asset import Asset
from homebroker.models.wallet import Wallet


class Order(BaseModel):
    """
    Model to store some order-related data.

    This model is used to store some order-related data.

    Attributes:
        user (`ForeignKey[User]`): The user who created the order.
        asset (`ForeignKey[Asset]`): The asset related to the order.
        wallet (`ForeignKey[Wallet]`): The wallet related to the order.
        shares (`DecimalField`): The number of shares related to the order.
        partial (`IntegerField`): The number of shares already bought.
        share_price (`DecimalField`): The price of a single share.
        total_price (`DecimalField`): The total price of the order.
        status (`CharField`): The status of the order.
        type (`CharField`): The type of the order.
    """

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    objects: OrderManager = OrderManager()

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
    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name=_("Wallet"),
        help_text=_("The wallet related to the order."),
    )
    shares = models.IntegerField(
        verbose_name=_("Shares"),
        help_text=_("The number of shares related to the order."),
    )
    partial = models.IntegerField(
        default=0,
        verbose_name=_("Partial"),
        help_text=_("The number of shares already bought."),
    )
    share_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Share price"),
        help_text=_("The price of a single share."),
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Price"),
        help_text=_("The total price of the order."),
    )
    status = models.CharField(
        max_length=10,
        choices=ORDER_STATUS_CHOICES.choices,
        default=ORDER_STATUS_CHOICES.OPEN,
        verbose_name=_("Status"),
        help_text=_("The status of the order."),
    )
    type = models.CharField(
        max_length=10,
        choices=ORDER_TYPE_CHOICES.choices,
        verbose_name=_("Type"),
        help_text=_("The type of the order."),
    )

    def increase_partial(self, shares: int) -> None:
        """
        Increase the partial shares.

        This method is used to increase the partial shares
        of the order and save the changes.

        Args:
            shares (`int`): The number of shares to increase.
        """
        self.partial += shares
        self.save(update_fields=("partial",))

        if self.partial == self.shares:
            self.close()

    def close(self) -> None:
        """
        Close the order.

        This method is used to update the order status to "closed"
        and save the changes.
        """
        self.status = ORDER_STATUS_CHOICES.CLOSED
        self.save(update_fields=("status",))
