"""
Module containing the Asset model.
"""

from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.mixins import BaseModel


class Asset(BaseModel):
    """
    Model to store some asset-related data.

    This model is used to store some asset-related data.

    Fields:
    -----------
        * `name`: `CharField`
            The name of the asset.

        * `symbol`: `CharField`
            The symbol of the asset.

        * `price`: `DecimalField`
            The price of the asset.

        * `image`: `URLField`
            The image url of the asset.
    """

    name = models.CharField(
        _("Name"),
        max_length=255,
        help_text=_("The name of the asset."),
    )
    symbol = models.CharField(
        _("Symbol"),
        max_length=10,
        help_text=_("The symbol of the product"),
    )
    price = models.DecimalField(
        _("Price"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal(0.0))],
        help_text=_("The price of the asset. Must be greater than or equal to 0."),
    )
    image = models.URLField(
        _("Image"),
        help_text=_("The image url of the asset."),
    )

    class Meta:
        verbose_name = "Asset"
        verbose_name_plural = "Assets"
