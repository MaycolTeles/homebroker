"""
Module containing the `WalletAdmin` class.
"""

from django.contrib import admin

from core.mixins import BaseAdmin
from homebroker.models import Wallet, WalletAsset


class _WalletAssetInline(admin.TabularInline):
    """
    Inline class for the WalletAsset model.
    """

    model = WalletAsset
    extra = 0


@admin.register(Wallet)
class WalletAdmin(BaseAdmin):
    """
    Admin class for the Wallet model.
    """

    list_display = (
        "name",
        "user",
    )
    search_fields = (
        "name",
        "user",
    )
    inlines = (_WalletAssetInline,)
