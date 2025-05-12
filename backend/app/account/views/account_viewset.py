"""
Module containing the Account views.
"""

from account.models import Account
from account.serializers import AccountSerializer
from core.mixins import BaseModelViewSet


class AccountViewSet(BaseModelViewSet):
    """
    API endpoint to define Account actions.

    The available actions for the Account model are:
    * List
    * Create
    * Retrieve
    * Update
    * Partial Update
    * Destroy
    """

    queryset = Account.objects.all()
    serializer_class = AccountSerializer
