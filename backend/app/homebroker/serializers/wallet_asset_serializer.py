"""
Module containing all the WalletAsset-related serializers.
"""

from rest_framework import serializers

from homebroker.models import WalletAsset


class WalletAssetSerializer(serializers.ModelSerializer):
    """
    Class to serialize the WalletAsset model.
    """

    class Meta:
        model = WalletAsset
        fields = "__all__"
