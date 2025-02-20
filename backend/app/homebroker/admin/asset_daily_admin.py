"""
Module containing the AssetDailyAdmin class.
"""

from django.contrib import admin

from core.mixins import BaseAdmin
from homebroker.models import AssetDaily


@admin.register(AssetDaily)
class AssetDailyAdmin(BaseAdmin):
    """
    Admin class for the AssetDaily model.
    """

    search_fields = (
        "asset",
        "date",
    )
    list_display = (
        "asset",
        "date",
    )
