"""
Module containing all the AssetDaily-related serializers.
"""

from rest_framework import serializers

from homebroker.models import AssetDaily


class AssetDailySerializer(serializers.ModelSerializer):
    """
    Class to serialize the AssetDaily model.
    """

    class Meta:
        model = AssetDaily
        fields = "__all__"
