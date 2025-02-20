"""
Module containing the WalletAsset views.
"""

from rest_framework.viewsets import ModelViewSet

from homebroker.models import WalletAsset
from homebroker.serializers import WalletAssetSerializer


class WalletAssetViewSet(ModelViewSet):
    """
    API endpoint to define WalletAsset actions/methods.

    The available actions for the WalletAsset model are:
    * List
    * Create
    * Retrieve
    * Update
    * Destroy
    """

    queryset = WalletAsset.objects.all()
    serializer_class = WalletAssetSerializer
