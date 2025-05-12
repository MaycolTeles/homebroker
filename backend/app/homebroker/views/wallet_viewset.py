"""
Module containing the Wallet views.
"""

from core.mixins import BaseModelViewSet
from core.shared import DRF_VIEWSET_ACTIONS
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
    * Partial Update
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
            `WalletSerializer`: The WalletSerializer class.
        """
        if self.action in DRF_VIEWSET_ACTIONS.DETAIL.value:
            return WalletDetailSerializer

        return WalletListSerializer
