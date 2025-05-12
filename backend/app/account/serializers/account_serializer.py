"""
Module containing the Account serializer.
"""

from rest_framework import serializers

from account.models import Account


class AccountSerializer(serializers.ModelSerializer):
    """
    Class to serialize the Account model.
    """

    class Meta:
        model = Account
        fields = "__all__"
