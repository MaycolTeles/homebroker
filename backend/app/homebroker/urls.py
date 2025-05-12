"""
Module containing all the URL patterns for the Homebroker app.
"""

from rest_framework import routers

from homebroker.views import (
    AssetDailyViewSet,
    AssetViewSet,
    OrderViewSet,
    WalletAssetViewSet,
    WalletViewSet,
)


router = routers.DefaultRouter()
router.register(r"assets", AssetViewSet, basename="assets")
router.register(r"assets-dailies", AssetDailyViewSet, basename="assets-dailies")
router.register(r"orders", OrderViewSet, basename="orders")
router.register(r"wallet-assets", WalletAssetViewSet, basename="wallet-assets")
router.register(r"wallets", WalletViewSet, basename="wallets")
