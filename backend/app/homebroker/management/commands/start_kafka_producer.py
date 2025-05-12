"""
Module containing the `start_kafka_producer` command.
"""

import json
import time
from datetime import timedelta

import djclick as click
from confluent_kafka import Producer


@click.command()
def start_kafka_producer() -> None:
    """
    Start the kafka producer.

    Generates new asset dailies and send a kafka message
    that the asset daily was created.
    """
    from core.constants import KAFKA_HOST
    from homebroker.kafka.topics import AssetDailyKafkaTopics
    from homebroker.models import AssetDaily

    config = {
        "bootstrap.servers": KAFKA_HOST,
        "enable.idempotence": True,
        "acks": "all",
        "retries": 5,
    }
    producer = Producer(config)

    topic = AssetDailyKafkaTopics.ASSET_DAILY_CREATED.value
    mult = -1

    for _ in range(5):
        mult *= -1
        ad = AssetDaily.objects.filter(asset__name="Amazon").order_by("datetime").last()
        new_price = ad.price + (20 * mult)
        new_datetime = ad.datetime + timedelta(minutes=1)

        new_ad = AssetDaily.objects.create(asset=ad.asset, datetime=new_datetime, price=new_price)

        msg = json.dumps({"asset_daily_id": str(new_ad.id)}).encode()
        producer.produce(topic, value=msg)
        producer.flush()
        time.sleep(2)
