"""
Module containing the Wallet serializer.
"""

from rest_framework import serializers

from homebroker.models import Wallet
from homebroker.serializers import WalletAssetSerializer


class WalletSerializer(serializers.ModelSerializer):
    """
    Class to serialize the Wallet model.
    """

    class Meta:
        model = Wallet
        fields = "__all__"


class WalletListSerializer(WalletSerializer):
    """
    Class to serialize all the Wallet model (list).
    """

    class Meta:
        model = Wallet
        fields = "__all__"


class WalletDetailSerializer(WalletSerializer):
    """
    Class to serialize a single Wallet model instance (detail).

    This serializer also includes the wallet assets.
    """

    assets = serializers.SerializerMethodField()

    def get_assets(self, obj: Wallet) -> dict[str, str]:
        """
        Method to get the wallet assets.

        Parameters:
        ----------
            obj: `Wallet`
                The wallet object.

        Returns:
        -------
            `dict[str, str]`: The wallet-assets instances.
        """
        serializer = WalletAssetSerializer(obj.assets, many=True)
        return serializer.data
