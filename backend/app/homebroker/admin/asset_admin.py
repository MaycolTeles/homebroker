"""
Module containing the AssetAdmin class.
"""

from django.contrib import admin

from core.mixins import BaseAdmin
from homebroker.models import Asset


@admin.register(Asset)
class AssetAdmin(BaseAdmin):
    """
    Admin class for the Asset model.
    """

    search_fields = (
        "name",
        "symbol",
        "price",
    )
    list_display = ("name", "symbol", "price")
