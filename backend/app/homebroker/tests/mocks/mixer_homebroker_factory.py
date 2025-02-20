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
    def create_asset(*args, **kwargs) -> Asset:
        """
        Return an instance of an Asset.
        """
        return _create_asset(*args, **kwargs)

    @staticmethod
    def create_asset_daily(*args, **kwargs) -> AssetDaily:
        """
        Return an instance of an AssetDaily.
        """
        return _create_asset_daily(*args, **kwargs)

    @staticmethod
    def create_order(*args, **kwargs) -> Order:
        """
        Return an instance of an Order.
        """
        return _create_order(*args, **kwargs)

    @staticmethod
    def create_wallet(*args, **kwargs) -> Wallet:
        """
        Return an instance of an Wallet.
        """
        return _create_wallet(*args, **kwargs)

    @staticmethod
    def create_wallet_asset(*args, **kwargs) -> WalletAsset:
        """
        Return an instance of an WalletAsset.
        """
        return _create_wallet_asset(*args, **kwargs)


def _create_asset(*args, **kwargs) -> Asset:
    """
    Create an asset instance using mixer.

    This function creates an asset instance using mixer and returns it.

    Parameters:
    -----------
        * args: `Tuple`
            The fields to be passed to the mixer instance.

        * kwargs: `Dict`
            The fields to be passed to the mixer instance.

    Returns:
    --------
        * `Asset`
            The asset instance created.
    """
    asset: Asset = mixer.blend(Asset, *args, **kwargs)  # type: ignore
    return asset


def _create_asset_daily(*args, **kwargs) -> AssetDaily:
    """
    Create an asset_daily instance using mixer.

    This function creates an asset_daily instance using mixer and returns it.

    Parameters:
    -----------
        * args: `Tuple`
            The fields to be passed to the mixer instance.

        * kwargs: `Dict`
            The fields to be passed to the mixer instance.

    Returns:
    --------
        * `AssetDaily`
            The asset_daily instance created.
    """
    asset_daily: AssetDaily = mixer.blend(AssetDaily, *args, **kwargs)  # type: ignore
    return asset_daily


def _create_order(*args, **kwargs) -> Order:
    """
    Create an order instance using mixer.

    This function creates an order instance using mixer and returns it.

    Parameters:
    -----------
        * args: `Tuple`
            The fields to be passed to the mixer instance.

        * kwargs: `Dict`
            The fields to be passed to the mixer instance.

    Returns:
    --------
        * `Order`
            The order instance created.
    """
    order: Order = mixer.blend(Order, *args, **kwargs)  # type: ignore
    return order


def _create_wallet(*args, **kwargs) -> Wallet:
    """
    Create an wallet instance using mixer.

    This function creates an wallet instance using mixer and returns it.

    Parameters:
    -----------
        * args: `Tuple`
            The fields to be passed to the mixer instance.

        * kwargs: `Dict`
            The fields to be passed to the mixer instance.

    Returns:
    --------
        * `Wallet`
            The wallet instance created.
    """
    wallet: Wallet = mixer.blend(Wallet, *args, **kwargs)  # type: ignore
    return wallet


def _create_wallet_asset(*args, **kwargs) -> WalletAsset:
    """
    Create an wallet_asset instance using mixer.

    This function creates an wallet_asset instance using mixer and returns it.

    Parameters:
    -----------
        * args: `Tuple`
            The fields to be passed to the mixer instance.

        * kwargs: `Dict`
            The fields to be passed to the mixer instance.

    Returns:
    --------
        * `WalletAsset`
            The wallet_asset instance created.
    """
    wallet_asset: WalletAsset = mixer.blend(WalletAsset, *args, **kwargs)  # type: ignore
    return wallet_asset
