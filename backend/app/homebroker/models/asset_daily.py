"""
Module containing the `AssetDaily` model.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.mixins import BaseModel
from core.shared import NonNegativeValueValidator
from homebroker.models import Asset


class AssetDaily(BaseModel):
    """
    Model to store some asset-daily-related data.

    This model is used to store some asset-daily-related data.

    Attributes:
        asset (`ForeignKey[Asset]`): The asset related to the asset-daily.
        datetime (`DateTimeField`): The datetime of the asset-daily.
        price (`DecimalField`): The asset price in that given time.
    """

    class Meta:
        verbose_name = "Asset Daily"
        verbose_name_plural = "Assets Dailies"

    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name="asset_dailies",
        verbose_name=_("Asset"),
        help_text=_("The asset related to the asset-daily."),
    )
    datetime = models.DateTimeField(
        _("Date"),
        help_text=_("The datetime of the asset-daily."),
    )
    price = models.DecimalField(
        _("Price"),
        max_digits=10,
        decimal_places=2,
        help_text=_("The price of the asset in that given time. Must be greater than or equal to 0."),
        validators=(NonNegativeValueValidator(),),
    )
