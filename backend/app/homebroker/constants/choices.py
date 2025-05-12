"""
Module containing all the constant choices for the Homebroker app.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class ORDER_STATUS_CHOICES(models.TextChoices):  # noqa: N801
    """
    Choices for the order status.
    """

    CLOSED = "CLOSED", _("Closed")  # Totally executed
    FAILED = "FAILED", _("Failed")  # Failed or cancelled by whatever reason
    OPEN = "OPEN", _("Open")  # Just created or partially executed


class ORDER_TYPE_CHOICES(models.TextChoices):  # noqa: N801
    """
    Choices for the order type.
    """

    BUY = "BUY", _("Buy")
    SELL = "SELL", _("Sell")
