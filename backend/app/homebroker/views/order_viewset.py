"""
Module containing the Order views.
"""

from core.mixins import BaseModelViewSet
from homebroker.filters import OrderFilter
from homebroker.models import Order
from homebroker.serializers import (
    OrderCreateSerializer,
    OrderDetailSerializer,
    OrderSerializer,
)


class OrderViewSet(BaseModelViewSet):
    """
    API endpoint to define Order actions/methods.

    The available actions for the Order model are:
    * List
    * Create
    * Retrieve
    * Update
    * Partial Update
    * Destroy
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filterset_class = OrderFilter

    def get_serializer_class(self) -> type[OrderSerializer]:
        """
        Method to get the serializer class.

        This method returns a OrderSerializer class
        based on the action/method.

        Returns:
            `OrderSerializer`: The OrderSerializer class.
        """
        if self.action == "create":
            return OrderCreateSerializer

        return OrderDetailSerializer
