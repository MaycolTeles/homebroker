"""
Module containing the Account admin.
"""

from django.contrib import admin

from account.models import Account
from core.mixins import BaseAdmin


@admin.register(Account)
class AccountAdmin(BaseAdmin):
    """
    Admin class for the Account model.
    """
