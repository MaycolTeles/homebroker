"""
Module containing the `task_create_default_assets_dailies` task.
"""

from datetime import timedelta

from celery import shared_task

from core.logger import get_logger
from core.shared import aware_datetime_now
from homebroker.models import Asset, AssetDaily


logger = get_logger(component="homebroker", subcomponent="tasks", task="task_create_default_assets_dailies")


@shared_task
def task_create_default_assets_dailies() -> None:
    """
    Creates all the default assets-dailies used in Homebroker app.

    This task creates 5 instances of AssetDaily model for each default asset in the app.

    It also assumes that all the Assets were created before, so make sure you
    have all the default assets instances created.
    """
    logger.info('task "task_create_default_assets_dailies" started.')

    try:
        assets_dailies = _get_all_assets_dailies()
        AssetDaily.objects.bulk_create(assets_dailies)

    except Exception:
        logger.exception("An error occurred while creating all the assets dailies.")

    logger.info('task "task_create_default_assets_dailies" finished.')


def _get_all_assets_dailies() -> tuple[AssetDaily, ...]:
    datetime_now = aware_datetime_now()
    datetime_1_min_ago = datetime_now - timedelta(minutes=1)
    datetime_5_min_ago = datetime_now - timedelta(minutes=2)
    datetime_10_min_ago = datetime_now - timedelta(minutes=3)
    datetime_20_min_ago = datetime_now - timedelta(minutes=4)

    amazon = Asset.objects.get(name="Amazon")
    asset_dailies_amazon = (
        AssetDaily(asset=amazon, datetime=datetime_20_min_ago, price=50.0),
        AssetDaily(asset=amazon, datetime=datetime_10_min_ago, price=55.0),
        AssetDaily(asset=amazon, datetime=datetime_5_min_ago, price=52.0),
        AssetDaily(asset=amazon, datetime=datetime_1_min_ago, price=48.0),
        AssetDaily(asset=amazon, datetime=datetime_now, price=50.0),
    )

    coca_cola = Asset.objects.get(name="Coca Cola")
    asset_dailies_coca_cola = (
        AssetDaily(asset=coca_cola, datetime=datetime_20_min_ago, price=40.0),
        AssetDaily(asset=coca_cola, datetime=datetime_10_min_ago, price=30.0),
        AssetDaily(asset=coca_cola, datetime=datetime_5_min_ago, price=25.0),
        AssetDaily(asset=coca_cola, datetime=datetime_1_min_ago, price=32.0),
        AssetDaily(asset=coca_cola, datetime=datetime_now, price=35.0),
    )

    google = Asset.objects.get(name="Google")
    asset_dailies_google = (
        AssetDaily(asset=google, datetime=datetime_20_min_ago, price=60.0),
        AssetDaily(asset=google, datetime=datetime_10_min_ago, price=70.0),
        AssetDaily(asset=google, datetime=datetime_5_min_ago, price=95.0),
        AssetDaily(asset=google, datetime=datetime_1_min_ago, price=85.0),
        AssetDaily(asset=google, datetime=datetime_now, price=80.0),
    )

    mc_donalds = Asset.objects.get(name="Mc Donalds")
    asset_dailies_mc_donalds = (
        AssetDaily(asset=mc_donalds, datetime=datetime_20_min_ago, price=45.0),
        AssetDaily(asset=mc_donalds, datetime=datetime_10_min_ago, price=35.0),
        AssetDaily(asset=mc_donalds, datetime=datetime_5_min_ago, price=30.0),
        AssetDaily(asset=mc_donalds, datetime=datetime_1_min_ago, price=27.0),
        AssetDaily(asset=mc_donalds, datetime=datetime_now, price=34.0),
    )

    mercado_livre = Asset.objects.get(name="Mercado Livre")
    asset_dailies_mercado_livre = (
        AssetDaily(asset=mercado_livre, datetime=datetime_20_min_ago, price=30.0),
        AssetDaily(asset=mercado_livre, datetime=datetime_10_min_ago, price=35.0),
        AssetDaily(asset=mercado_livre, datetime=datetime_5_min_ago, price=32.0),
        AssetDaily(asset=mercado_livre, datetime=datetime_1_min_ago, price=24.0),
        AssetDaily(asset=mercado_livre, datetime=datetime_now, price=20.0),
    )

    meta = Asset.objects.get(name="Meta")
    asset_dailies_meta = (
        AssetDaily(asset=meta, datetime=datetime_20_min_ago, price=70.0),
        AssetDaily(asset=meta, datetime=datetime_10_min_ago, price=80.0),
        AssetDaily(asset=meta, datetime=datetime_5_min_ago, price=90.0),
        AssetDaily(asset=meta, datetime=datetime_1_min_ago, price=110.0),
        AssetDaily(asset=meta, datetime=datetime_now, price=90.0),
    )

    nvidia = Asset.objects.get(name="Nvidia")
    asset_dailies_nvidia = (
        AssetDaily(asset=nvidia, datetime=datetime_20_min_ago, price=55.0),
        AssetDaily(asset=nvidia, datetime=datetime_10_min_ago, price=75.0),
        AssetDaily(asset=nvidia, datetime=datetime_5_min_ago, price=105.0),
        AssetDaily(asset=nvidia, datetime=datetime_1_min_ago, price=125.0),
        AssetDaily(asset=nvidia, datetime=datetime_now, price=100.0),
    )

    salesforce = Asset.objects.get(name="Salesforce")
    asset_dailies_salesforce = (
        AssetDaily(asset=salesforce, datetime=datetime_20_min_ago, price=35.0),
        AssetDaily(asset=salesforce, datetime=datetime_10_min_ago, price=55.0),
        AssetDaily(asset=salesforce, datetime=datetime_5_min_ago, price=60.0),
        AssetDaily(asset=salesforce, datetime=datetime_1_min_ago, price=53.0),
        AssetDaily(asset=salesforce, datetime=datetime_now, price=49.0),
    )

    assets_dailies = (
        *asset_dailies_amazon,
        *asset_dailies_coca_cola,
        *asset_dailies_google,
        *asset_dailies_mc_donalds,
        *asset_dailies_mercado_livre,
        *asset_dailies_meta,
        *asset_dailies_nvidia,
        *asset_dailies_salesforce,
    )

    return assets_dailies
