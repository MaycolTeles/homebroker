"""
Module containing the Wallet FilterSet.
"""

from django_filters import rest_framework as filters

from homebroker.models import Wallet


class WalletFilter(filters.FilterSet):
    """
    Class to filter the Wallet model.
    """

    name = filters.CharFilter(field_name="name", lookup_expr="icontains", label="Name Contains")

    ordering = filters.OrderingFilter(
        fields=(("name", "name"),),
    )

    class Meta:
        model = Wallet
        fields = ("name",)
