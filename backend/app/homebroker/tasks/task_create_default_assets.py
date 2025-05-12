"""
Module containing the `task_create_default_assets` task.
"""

from celery import shared_task

from core.logger import get_logger
from homebroker.models import Asset


logger = get_logger(component="homebroker", subcomponent="tasks", task="task_create_default_assets")


@shared_task
def task_create_default_assets() -> None:
    """
    Creates all the default assets used in Homebroker app.

    The default assets are the 8 listed below:
        * Amazon
        * Coca Cola
        * Google
        * Mc Donalds
        * Mercado Livre
        * Meta
        * Nvidia
        * Salesforce
    """
    logger.info('task "task_create_default_assets" started.')

    try:
        Asset.objects.bulk_create(ASSETS)

    except Exception:
        logger.exception("An error occurred while creating all the assets.")

    logger.info('task "task_create_default_assets" finished.')


_BASE_IMAGE_URL = "https://raw.githubusercontent.com/devfullcycle/imersao21/refs/heads/main/nestjs-api/assets/{}.png"


ASSETS = (
    Asset(name="Amazon", symbol="AMZN", price=50.0, image_url=_BASE_IMAGE_URL.format("AMZN")),
    Asset(name="Coca Cola", symbol="COCA", price=40.0, image_url=_BASE_IMAGE_URL.format("KO")),
    Asset(name="Google", symbol="GOOG", price=60.0, image_url=_BASE_IMAGE_URL.format("GOOGL")),
    Asset(name="Mc Donalds", symbol="MCDN", price=45.0, image_url=_BASE_IMAGE_URL.format("MCD")),
    Asset(name="Mercado Livre", symbol="MELI", price=30.0, image_url=_BASE_IMAGE_URL.format("MELI")),
    Asset(name="Meta", symbol="META", price=70.0, image_url=_BASE_IMAGE_URL.format("META")),
    Asset(name="Nvidia", symbol="NVDA", price=55.0, image_url=_BASE_IMAGE_URL.format("NVDA")),
    Asset(name="Salesforce", symbol="SFRC", price=35.0, image_url=_BASE_IMAGE_URL.format("CRM")),
)
