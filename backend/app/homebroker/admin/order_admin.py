"""
Module containing the OrderAdmin class.
"""

from django.contrib import admin

from core.mixins import BaseAdmin
from homebroker.models import Order


@admin.register(Order)
class OrderAdmin(BaseAdmin):
    """
    Admin class for the Order model.
    """

    search_fields = (
        "user",
        "shares",
        "partial",
        "price",
        "status",
        "type",
    )
    list_display = (
        "user",
        "shares",
        "partial",
        "price",
        "status",
        "type",
    )
