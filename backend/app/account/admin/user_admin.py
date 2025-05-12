"""
Module containing the User admin.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Model
from django.http import HttpRequest

from account.models import User
from core.mixins import BaseAdmin, FieldsetType


@admin.register(User)
class UserAdmin(BaseUserAdmin, BaseAdmin):
    """
    Admin class for the User model.
    """

    search_fields = ("email", "username", "first_name")
    list_display = ("username", "email")

    def get_fieldsets(self, request: HttpRequest, obj: Model) -> list[FieldsetType]:
        """
        Merge BaseUserAdmin's default fieldsets with BaseAdmin's logic.

        This is used in order to display all `User` model fields in admin
        while keeping the layout/design defined in `BaseUserAdmin` class.
        """
        # Get BaseUserAdmin's fieldsets
        user_admin_fieldsets = super(BaseUserAdmin, self).get_fieldsets(request, obj)

        # Dynamically get all fields from the User model
        user_model_fields = {field.name for field in self.model._meta.fields}  # noqa: SLF001

        # Exclude fields already present in BaseUserAdmin to avoid duplication
        existing_fields = {field for fs in user_admin_fieldsets for field in fs[1]["fields"]}
        new_fields = user_model_fields - existing_fields

        # Add user custom fields (e.g., birthdate, current_balance)
        # to the second fieldset (the User details section)
        user_admin_fieldsets[1][1]["fields"] += tuple(new_fields)

        return user_admin_fieldsets
