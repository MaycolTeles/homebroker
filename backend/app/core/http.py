"""
Module containing the `BearerTokenAuthentication` class.
"""

from rest_framework.authentication import TokenAuthentication


class BearerTokenAuthentication(TokenAuthentication):
    """
    Class to set the TokenAuthentication method keyword to "Bearer".
    """

    keyword = "Bearer"
