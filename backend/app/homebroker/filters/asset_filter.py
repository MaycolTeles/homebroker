"""
Module containing the Asset FilterSet.
"""

from django_filters import rest_framework as filters

from homebroker.models import Asset


class AssetFilter(filters.FilterSet):
    """
    Class to filter the Asset model.
    """

    name = filters.CharFilter(field_name="name", lookup_expr="icontains", label="Name Contains")
    symbol = filters.CharFilter(field_name="symbol", lookup_expr="icontains", label="Symbol Contains")

    price__lt = filters.NumberFilter(field_name="price", lookup_expr="lt", label="Price Less Than")
    price__lte = filters.NumberFilter(field_name="price", lookup_expr="lte", label="Price Less Than or Equal To")
    price__gte = filters.NumberFilter(field_name="price", lookup_expr="gte", label="Price Greater Than or Equal To")
    price__gt = filters.NumberFilter(field_name="price", lookup_expr="gt", label="Price Greater Than")

    ordering = filters.OrderingFilter(
        fields=(
            ("name", "name"),
            ("symbol", "symbol"),
            ("price", "price"),
        ),
    )

    class Meta:
        model = Asset
        fields = ("name", "symbol", "price")
