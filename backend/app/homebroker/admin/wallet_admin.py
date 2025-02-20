"""
Module containing the WalletAdmin class.
"""

from django.contrib import admin

from core.mixins import BaseAdmin
from homebroker.models import Wallet


@admin.register(Wallet)
class WalletAdmin(BaseAdmin):
    """
    Admin class for the Wallet model.
    """

    list_display = (
        "user",
        "name",
    )
    search_fields = (
        "user",
        "name",
    )
