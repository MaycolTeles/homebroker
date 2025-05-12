"""
Module containing the AssetDaily FilterSet.
"""

from django_filters import rest_framework as filters

from homebroker.models import AssetDaily


class AssetDailyFilter(filters.FilterSet):
    """
    Class to filter the AssetDaily model.
    """

    asset = filters.CharFilter(field_name="asset")

    ordering = filters.OrderingFilter(
        fields=(
            ("price", "price"),
            ("datetime", "datetime"),
        ),
    )

    class Meta:
        model = AssetDaily
        fields = ("asset",)
