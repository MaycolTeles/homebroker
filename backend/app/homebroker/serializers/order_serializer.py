"""
Module containing the Order serializer.
"""

from rest_framework import serializers

from homebroker.models import Order


class OrderSerializer(serializers.ModelSerializer):
    """
    Class to serialize the Order model.
    """

    class Meta:
        model = Order
        fields = "__all__"
