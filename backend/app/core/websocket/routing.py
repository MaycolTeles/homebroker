"""
Module containing all the websocket routes from all local apps.
"""

from homebroker.websocket import homebroker_websocket_urlpatterns


websocket_urlpatterns = (*homebroker_websocket_urlpatterns,)
