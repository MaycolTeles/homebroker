"""
Module for the homebroker app configuration.
"""

from django.apps import AppConfig


class HomebrokerConfig(AppConfig):
    """
    Homebroker app configuration class.

    This class defines the configuration for the homebroker app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "homebroker"
