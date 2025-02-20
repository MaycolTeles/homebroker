"""
Module containing the AssetDaily views.
"""

from rest_framework.viewsets import ModelViewSet

from homebroker.models import AssetDaily
from homebroker.serializers import AssetDailySerializer


class AssetDailyViewSet(ModelViewSet):
    """
    API endpoint to define AssetDaily actions/methods.

    The available actions for the AssetDaily model are:
    * List
    * Create
    * Retrieve
    * Update
    * Destroy
    """

    queryset = AssetDaily.objects.all()
    serializer_class = AssetDailySerializer
