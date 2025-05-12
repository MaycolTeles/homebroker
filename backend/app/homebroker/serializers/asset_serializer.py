"""
Module containing all the Asset-related serializers.
"""

from rest_framework import serializers

from homebroker.models import Asset


class AssetSerializer(serializers.ModelSerializer):
    """
    Class to serialize the Asset model.
    """

    class Meta:
        model = Asset
        fields = "__all__"
