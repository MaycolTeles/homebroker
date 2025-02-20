"""
Module containing the Order views.
"""

from core.mixins import BaseModelViewSet
from homebroker.models import Order
from homebroker.serializers import OrderSerializer


class OrderViewSet(BaseModelViewSet):
    """
    API endpoint to define Order actions/methods.

    The available actions for the Order model are:
    * List
    * Create
    * Retrieve
    * Update
    * Destroy
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
