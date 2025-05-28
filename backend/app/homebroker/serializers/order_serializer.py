"""
Module containing all the Order-related serializers.
"""

from typing import Any

from rest_framework import serializers

from homebroker.models import Order
from homebroker.serializers.asset_serializer import AssetSerializer


class OrderSerializer(serializers.ModelSerializer):
    """
    Class to serialize the Order model.
    """

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ("total_price",)

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def update(self, instance: Order, validated_data: dict[str, Any]) -> Order:
        """
        Update the order instance.

        Calls the `update()` method from the OrderManager.

        Args:
            instance (`Order`): The order instance that will be updated.
            validated_data (`dict[str, Any]`): The new and already validated data to replace the old order data.

        Returns:
            `Order`: The updated order.
        """
        return Order.objects.update(instance, **validated_data)


class OrderCreateSerializer(OrderSerializer):
    """
    Class to serialize all the Order model (list).
    """


class OrderDetailSerializer(OrderSerializer):
    """
    Class to serialize a single Order model instance (detail).

    This serializer also includes the asset details.
    """

    asset = AssetSerializer(read_only=True)
