"""
Module containing all the Websocket URL patterns for the Homebroker app.
"""

from django.urls import path

from homebroker.websocket.consumers import AssetWebsocketConsumer


homebroker_websocket_urlpatterns = (path("ws/assets/<uuid:asset_id>/", AssetWebsocketConsumer.as_asgi()),)
