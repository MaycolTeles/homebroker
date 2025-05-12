"""
Module containing the `Asset` model.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.mixins import BaseModel
from core.shared import NonNegativeValueValidator


class Asset(BaseModel):
    """
    Model to store some asset-related data.

    This model is used to store some asset-related data.

    Attributes:
        name (`CharField`): The name of the asset.
        symbol (`CharField`): The symbol of the asset.
        price (`DecimalField`): The price of the asset.
        image_url (`URLField`): The image url of the asset.
    """

    class Meta:
        verbose_name = "Asset"
        verbose_name_plural = "Assets"

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
        help_text=_("The price of the asset. Must be greater than or equal to 0."),
        validators=(NonNegativeValueValidator(),),
    )
    image_url = models.URLField(
        _("Image URL"),
        help_text=_("The image url of the asset."),
    )

    def __str__(self) -> str:
        """
        Return the asset name.
        """
        return self.name
