"""
Module containing the MixerHomebrokerFactory class.
"""

from mixer.backend.django import mixer

from homebroker.models import (
    Asset,
    AssetDaily,
    Order,
    Wallet,
    WalletAsset,
)


class MixerHomebrokerFactory:
    """
    Class responsible for creating instances of the models.

    This class provides a set of static methods that create instances
    of all the models in the homebroker app.
    """

    @staticmethod
    def create_asset(**kwargs) -> Asset:
        """
        Return an instance of an Asset.
        """
        return _create_asset(**kwargs)

    @staticmethod
    def create_asset_daily(**kwargs) -> AssetDaily:
        """
        Return an instance of an AssetDaily.
        """
        return _create_asset_daily(**kwargs)

    @staticmethod
    def create_order(**kwargs) -> Order:
        """
        Return an instance of an Order.
        """
        return _create_order(**kwargs)

    @staticmethod
    def create_wallet(**kwargs) -> Wallet:
        """
        Return an instance of an Wallet.
        """
        return _create_wallet(**kwargs)

    @staticmethod
    def create_wallet_asset(**kwargs) -> WalletAsset:
        """
        Return an instance of an WalletAsset.
        """
        return _create_wallet_asset(**kwargs)


def _create_asset(**kwargs) -> Asset:
    """
    Create an asset instance using mixer.

    This function creates an asset instance using mixer and returns it.

    Args:
        kwargs `dict[str, Any]`: The fields to be passed to the mixer instance.

    Returns:
        `Asset`: The asset instance created.
    """
    asset: Asset = mixer.blend(Asset, **kwargs)  # type: ignore
    return asset


def _create_asset_daily(**kwargs) -> AssetDaily:
    """
    Create an asset_daily instance using mixer.

    This function creates an asset_daily instance using mixer and returns it.

    Args:
        kwargs `dict[str, Any]`: The fields to be passed to the mixer instance.

    Returns:
        * `AssetDaily`: The asset_daily instance created.
    """
    asset_daily: AssetDaily = mixer.blend(AssetDaily, **kwargs)  # type: ignore
    return asset_daily


def _create_order(**kwargs) -> Order:
    """
    Create an order instance using mixer.

    This function creates an order instance using mixer and returns it.

    Args:
        kwargs `dict[str, Any]`: The fields to be passed to the mixer instance.

    Returns:
        * `Order`: The order instance created.
    """
    order: Order = mixer.blend(Order, **kwargs)  # type: ignore
    return order


def _create_wallet(**kwargs) -> Wallet:
    """
    Create an wallet instance using mixer.

    This function creates an wallet instance using mixer and returns it.

    Args:
        kwargs `dict[str, Any]`: The fields to be passed to the mixer instance.

    Returns:
        * `Wallet`: The wallet instance created.
    """
    wallet: Wallet = mixer.blend(Wallet, **kwargs)  # type: ignore
    return wallet


def _create_wallet_asset(**kwargs) -> WalletAsset:
    """
    Create an wallet_asset instance using mixer.

    This function creates an wallet_asset instance using mixer and returns it.

    Args:
        kwargs `dict[str, Any]`: The fields to be passed to the mixer instance.

    Returns:
        * `WalletAsset`: The wallet_asset instance created.
    """
    wallet_asset: WalletAsset = mixer.blend(WalletAsset, **kwargs)  # type: ignore
    return wallet_asset
