"""
Module containing the `start_homebroker_kafka_consumer` command.
"""

import djclick as click

from core.logger import get_logger
from homebroker.kafka import (
    start_asset_daily_consumer,
)


logger = get_logger(component="homebroker", subcomponent="commands", command="start_homebroker_kafka_consumer")


CONSUMERS_MAP = {"asset_daily": start_asset_daily_consumer}


@click.command()
@click.argument("consumer")
def start_homebroker_kafka_consumer(consumer: str) -> None:
    """
    Start a Homebroker Kafka Consumer.

    To execute this command, run the following command:

    .. code-block:: bash
        $ python manage.py start_homebroker_consumer <consumer>

    For example:

    .. code-block:: bash
        $ python manage.py start_homebroker_consumer asset_daily
    ```
    """
    logger.info("Starting Homebroker Kafka Consumer.", consumer=consumer)

    start_consumer_function = CONSUMERS_MAP.get(consumer)
    if not start_consumer_function:
        msg = "Not a valid consumer. Choose one from the available options."
        logger.error(msg, consumer=consumer, available_options=CONSUMERS_MAP.keys())
        return

    try:
        start_consumer_function()

    except Exception:
        logger.exception("An error occurred while starting Homebroker Kafka Consumer.", consumer=consumer)
