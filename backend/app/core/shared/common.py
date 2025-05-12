"""
Module containing some common utilities.
"""

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any


class DRF_VIEWSET_ACTIONS(Enum):  # noqa: N801
    """
    Enum containing the DRF ViewSet actions.
    """

    DETAIL = ("retrieve", "update", "partial_update", "destroy")
    LIST = ("list", "create")


@dataclass
class DTO:
    """
    Generic DTO class.

    This class should be inherited by all
    DTO classes that wants the share the methods defined in it.
    """

    def to_json(self) -> dict[str, Any]:
        """
        Return the dataclass in a json (dict) format.
        """
        return asdict(self)
