"""
Module containing the Asset views.
"""

from rest_framework.viewsets import ModelViewSet

from homebroker.filters import AssetFilter
from homebroker.models import Asset
from homebroker.serializers import AssetSerializer


class AssetViewSet(ModelViewSet):
    """
    API endpoint to define Asset actions/methods.

    The available actions for the Asset model are:
    * List
    * Create
    * Retrieve
    * Update
    * Partial Update
    * Destroy
    """

    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    filterset_class = AssetFilter
