"""
Module containing the `start_asset_daily_consumer` function.
"""

import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from confluent_kafka import Consumer

from core.logger import get_logger
from homebroker.kafka.common import get_kafka_config
from homebroker.kafka.topics import AssetDailyKafkaTopics
from homebroker.models import AssetDaily


logger = get_logger(component="homebroker", subcomponent="kafka", consumer="asset_daily_consumer")


def start_asset_daily_consumer() -> None:
    """
    Start the asset daily kafka consumer.
    """
    config = get_kafka_config("asset-daily-group")
    consumer = Consumer(config)

    topics = [
        AssetDailyKafkaTopics.ASSET_DAILY_CREATED.value,
    ]
    consumer.subscribe(topics)

    logger.info("Starting Asset Daily Consumer...")

    try:
        while True:
            _run_kafka_consumer(consumer)

    except Exception:
        logger.exception("Error in Asset Daily Consumer")

    finally:
        consumer.close()


def _run_kafka_consumer(consumer: Consumer) -> None:
    msg = consumer.poll(1.0)
    if msg is None:
        return

    error = msg.error()
    if error:
        logger.error("Error when running asset daily consumer.", error=error)
        return

    data = json.loads(msg.value().decode())
    asset_daily_id = data.get("asset_daily_id")
    if not asset_daily_id:
        logger.error('No "asset_daily_id" found in the message', message=msg)
        return

    _send_asset_daily_id_to_websocket_consumer(asset_daily_id)


def _send_asset_daily_id_to_websocket_consumer(asset_daily_id: str) -> None:
    try:
        asset_daily = AssetDaily.objects.get(id=asset_daily_id)

    except AssetDaily.DoesNotExist:
        logger.exception("Unable to locate asset daily with given id.", asset_daily_id=asset_daily_id)
        return

    channel_layer = get_channel_layer()

    asset_id = str(asset_daily.asset.id)
    group_name = f"asset_{asset_id}"

    data = {"asset_daily_id": str(asset_daily.id)}
    event = {
        "type": "broadcast_asset_daily_created",
        "data": data,
    }

    async_to_sync(channel_layer.group_send)(group_name, event)
