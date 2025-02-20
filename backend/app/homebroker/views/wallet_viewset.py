"""
Module containing the Wallet views.
"""

from rest_framework.exceptions import MethodNotAllowed

from core.common import DRF_VIEWSET_ACTIONS
from core.mixins import BaseModelViewSet
from homebroker.filters import WalletFilter
from homebroker.models import Wallet
from homebroker.serializers import (
    WalletDetailSerializer,
    WalletListSerializer,
    WalletSerializer,
)


class WalletViewSet(BaseModelViewSet):
    """
    API endpoint to define Wallet actions/methods.

    The available actions for the Wallet model are:
    * List
    * Create
    * Retrieve
    * Update
    * Destroy
    """

    queryset = Wallet.objects.all()
    filterset_class = WalletFilter

    def get_serializer_class(self) -> type[WalletSerializer]:
        """
        Method to get the serializer class.

        This method returns a WalletSerializer class
        based on the action/method.

        Returns:
        -------
            `WalletSerializer`: The WalletSerializer class.
        """
        if self.action == DRF_VIEWSET_ACTIONS.LIST.value:
            return WalletListSerializer

        if self.action == DRF_VIEWSET_ACTIONS.RETRIEVE.value:
            return WalletDetailSerializer

        error_message = f"Unknown action: {self.action}"
        raise MethodNotAllowed(error_message)
