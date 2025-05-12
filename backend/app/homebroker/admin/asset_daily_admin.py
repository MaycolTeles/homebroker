"""
Module containing the `AssetDailyAdmin` class.
"""

from django.contrib import admin
from django.db.models import QuerySet
from rest_framework.request import Request

from core.mixins import BaseAdmin
from homebroker.models import AssetDaily


@admin.register(AssetDaily)
class AssetDailyAdmin(BaseAdmin):
    """
    Admin class for the AssetDaily model.
    """

    search_fields = (
        "asset",
        "datetime",
    )
    list_display = ("asset__name", "datetime", "price")
    list_filter = ("asset__name",)

    actions = ("generate_assets_dailies",)

    @admin.action(description="Create Asset Dailies")
    def generate_assets_dailies(self, request: Request, queryset: QuerySet[AssetDaily]) -> None:
        """
        Action to generate asset dailies.
        """
        from homebroker.tasks import task_generate_asset_dailies

        task_generate_asset_dailies.delay()
