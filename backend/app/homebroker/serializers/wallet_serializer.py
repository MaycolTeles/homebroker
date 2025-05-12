"""
Module containing all the Wallet-related serializers.
"""

from rest_framework import serializers

from homebroker.models import Wallet
from homebroker.serializers import WalletAssetSerializer


class WalletSerializer(serializers.ModelSerializer):
    """
    Class to serialize the Wallet model.
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    performance = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Wallet
        fields = "__all__"
        read_only_fields = ("total_invested", "current_balance")


class WalletListSerializer(WalletSerializer):
    """
    Class to serialize all the Wallet model (list).
    """


class WalletDetailSerializer(WalletSerializer):
    """
    Class to serialize a single Wallet model instance (detail).

    This serializer also includes the wallet assets details.
    """

    assets = WalletAssetSerializer(many=True, read_only=True)
