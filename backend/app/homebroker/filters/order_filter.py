"""
Module containing the Order FilterSet.
"""

from django_filters import rest_framework as filters

from homebroker.constants import ORDER_STATUS_CHOICES, ORDER_TYPE_CHOICES
from homebroker.models import Order


class OrderFilter(filters.FilterSet):
    """
    Class to filter the Order model.
    """

    asset = filters.CharFilter(field_name="asset", label="Asset ID")

    status = filters.ChoiceFilter(choices=ORDER_STATUS_CHOICES, label="Status is")

    type = filters.ChoiceFilter(choices=ORDER_TYPE_CHOICES, label="Type is")

    shares__lt = filters.NumberFilter(field_name="shares", lookup_expr="lt", label="Shares Less Than")
    shares__lte = filters.NumberFilter(field_name="shares", lookup_expr="lte", label="Shares Less Than or Equal To")
    shares__gte = filters.NumberFilter(field_name="shares", lookup_expr="gte", label="Shares Greater Than or Equal To")
    shares__gt = filters.NumberFilter(field_name="shares", lookup_expr="gt", label="Shares Greater Than")

    share_price__lt = filters.NumberFilter(field_name="share_price", lookup_expr="lt", label="Share price Less Than")
    share_price__lte = filters.NumberFilter(
        field_name="share_price", lookup_expr="lte", label="Share price Less Than or Equal To"
    )
    share_price__gte = filters.NumberFilter(
        field_name="share_price", lookup_expr="gte", label="Share price Greater Than or Equal To"
    )
    share_price__gt = filters.NumberFilter(field_name="share_price", lookup_expr="gt", label="Share price Greater Than")

    ordering = filters.OrderingFilter(
        fields=(
            ("asset", "asset"),
            ("status", "status"),
            ("type", "type"),
            ("shares", "shares"),
            ("share_price", "share_price"),
        ),
    )

    class Meta:
        model = Order
        fields = ("asset", "status", "type", "shares", "share_price")
