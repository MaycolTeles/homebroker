"""
Module containing all the kafka topics enums.
"""

from enum import Enum


class AssetDailyKafkaTopics(Enum):
    """
    Class to define Kafka topics for Asset Daily methods.
    """

    # Topic for Asset Daily creation
    ASSET_DAILY_CREATED = "asset_daily.created"
