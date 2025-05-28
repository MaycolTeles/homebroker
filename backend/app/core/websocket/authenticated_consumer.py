"""
Module containing the `AuthenticatedConsumer` class.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional
from urllib.parse import parse_qs

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.layers import BaseChannelLayer

from core.logger import get_logger


if TYPE_CHECKING:
    from account.models import User


logger = get_logger(component="core", subcomponent="websocket", consumer="AuthenticatedConsumer")


class AuthenticatedConsumer(AsyncJsonWebsocketConsumer):
    """
    Class to handle authenticated WebSocket connections.

    This class is used to authenticate users based on a token passed in the query string or headers.
    If the token is valid, the user is authenticated and the connection is accepted.

    The token is the same as the one used in the REST API,
    and it is expected to be passed in the query string or headers.
    """

    channel_layer: BaseChannelLayer  # Type hint for the channel layer

    async def connect(self) -> None:
        """
        Connect a new websocket client to the server group.

        First, it validates if the auth token is valid.
        The token can be passed either by headers or as a query string.
        If the token is not valid, closes the connection.
        """
        token = self._get_token()
        if not token:
            logger.warning("Token not found in query string or headers")
            await self.close()
            return

        user = await self._get_user_from_token(token)
        if not user:
            await self.close()
            return

        self.scope["user"] = user
        await self.accept()

    def _get_token(self) -> Optional[str]:
        token = self._get_token_from_querystring()

        if not token:
            token = self._get_token_from_headers()

        return token

    def _get_token_from_querystring(self) -> Optional[str]:
        query_string = self.scope.get("query_string", b"").decode()
        query_params = parse_qs(query_string)
        token = query_params.get("Authorization")

        return token[0] if token else None

    def _get_token_from_headers(self) -> Optional[str]:
        headers = {k.decode(): v.decode() for k, v in self.scope.get("headers", [])}
        token: str = headers.get("authorization", "")

        if not token:
            return None

        return token

    async def _get_user_from_token(self, token_key: str) -> Optional[User]:
        from rest_framework.authtoken.models import Token

        try:
            token_obj = await Token.objects.select_related("user").aget(key=token_key)

        except Token.DoesNotExist:
            logger.exception("Token does not exist", token=token_key)
            return None

        return token_obj.user
