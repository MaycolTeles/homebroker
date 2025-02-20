"""
Module containing some common utilities.
"""

from enum import Enum


class DRF_VIEWSET_ACTIONS(Enum):  # noqa: N801
    """
    Enum containing the DRF ViewSet actions.
    """

    LIST = "list"
    RETRIEVE = "retrieve"
