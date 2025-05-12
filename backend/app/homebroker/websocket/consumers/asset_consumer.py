"""
Module containing the AssetWebsocketConsumer class.
"""

from typing import Any

from asgiref.sync import sync_to_async

from core.websocket.authenticated_consumer import AuthenticatedConsumer


class AssetWebsocketConsumer(AuthenticatedConsumer):
    """
    Class containing all the code for the Asset Websocket Consumer.

    This consumer allow clients to connect to it throught a websocket connection
    and receive new asset data (new `AssetDaily` instances) or to send a request to
    buy/sell that asset.
    """

    group_name = None

    async def connect(self) -> None:
        """
        Connect a new websocket client to the server group.
        """
        asset_id = self.scope["url_route"]["kwargs"]["asset_id"]
        asset_exists = await self._check_if_asset_exists(asset_id)

        if not asset_exists:
            await self.close()
            return

        await super().connect()

        self.group_name = f"asset_{asset_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)

    async def disconnect(self, close_code: str) -> None:
        """
        Disconnect a websocket client from the server.
        """
        if self.group_name and self.channel_name:
            # Leave the group when the consumer disconnects
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content: dict[str, Any]) -> None:
        """
        Receive a JSON message from the websocket client.
        """

    async def broadcast_asset_daily_created(self, event: dict[str, Any]) -> None:
        """
        Broadcast the new asset daily through the websocket.

        This method assumes that the `event` param is valid and has valid data,
        so it doesn't do any validation - just assume everything is correct and
        sends the data through the websocket.
        """
        asset_daily_id = event["data"]["asset_daily_id"]
        asset_daily_data = await self._get_asset_daily_data(asset_daily_id)

        await self.send_json(asset_daily_data)

    async def _check_if_asset_exists(self, asset_id: str) -> bool:
        from homebroker.models import Asset

        @sync_to_async
        def _check() -> bool:
            return Asset.objects.filter(id=asset_id).exists()

        return await _check()

    async def _get_asset_daily_data(self, asset_daily_id: str) -> dict[str, Any]:
        from homebroker.models import AssetDaily
        from homebroker.serializers import AssetDailySerializer

        @sync_to_async
        def _get() -> dict[str, Any]:
            asset_daily = AssetDaily.objects.get(id=asset_daily_id)
            return AssetDailySerializer(asset_daily).data  # type: ignore

        return await _get()
