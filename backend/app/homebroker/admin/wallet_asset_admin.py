"""
Module containing the WalletAssetAdmin class.
"""

from django.contrib import admin

from core.mixins import BaseAdmin
from homebroker.models import WalletAsset


@admin.register(WalletAsset)
class WalletAssetAdmin(BaseAdmin):
    """
    Admin class for the WalletAsset model.
    """

    search_fields = (
        "wallet",
        "asset",
        "shares",
    )
    list_display = (
        "wallet",
        "asset",
        "shares",
    )
