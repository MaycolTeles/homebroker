"""
Module containing all the constant choices for the Homebroker app.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class ORDER_STATUS_CHOICES(models.TextChoices):  # noqa: N801
    """
    Choices for the order status.
    """

    CLOSED = "closed", _("Closed")
    FAILED = "failed", _("Failed")
    OPEN = "open", _("Open")
    PENDING = "pending", _("Pending")


class ORDER_TYPE_CHOICES(models.TextChoices):  # noqa: N801
    """
    Choices for the order type.
    """

    BUY = "buy", _("Buy")
    SELL = "sell", _("Sell")
