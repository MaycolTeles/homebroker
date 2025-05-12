"""
Module containing the common configs for kafka.
"""

from core.constants import KAFKA_HOST


def get_kafka_config(group_id: str) -> dict[str, str]:
    """
    Return the default Kafka configuration data.
    """
    return {
        "bootstrap.servers": KAFKA_HOST,
        "group.id": group_id,
        "auto.offset.reset": "earliest",
    }
