"""
Module containing the AssetDaily model.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.mixins import BaseModel
from homebroker.models import Asset


class AssetDaily(BaseModel):
    """
    Model to store some asset-daily-related data.

    This model is used to store some asset-daily-related data.

    Fields:
    -----------
        * `asset`: `ForeignKey[Asset]`
            The asset related to the asset-daily.

        * `date`: `DateTimeField`
            The date of the asset-daily.
    """

    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name="asset_dailies",
        verbose_name=_("Asset"),
        help_text=_("The asset related to the asset-daily."),
    )
    date = models.DateTimeField(
        _("Date"),
        help_text=_("The date of the asset-daily."),
    )

    class Meta:
        verbose_name = "AssetDaily"
        verbose_name_plural = "AssetDailies"
