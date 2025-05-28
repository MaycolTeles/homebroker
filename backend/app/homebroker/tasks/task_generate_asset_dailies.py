"""
Module containing the `task_generate_asset_dailies` task.
"""

import random
from datetime import timedelta

from celery import shared_task

from homebroker.models import Asset, AssetDaily


@shared_task
def task_generate_asset_dailies() -> None:
    """
    Task to generate some new asset dailies instances.
    """
    for _ in range(10):
        # Create a new asset daily for each asset
        for asset in Asset.objects.all():
            last_asset_daily = AssetDaily.objects.filter(asset=asset).order_by("-datetime").first()

            next_date = last_asset_daily.datetime + timedelta(hours=1)

            random_price_variation = random.randint(5, 10)  # noqa: S311
            random_price = random.randint(-random_price_variation, random_price_variation)  # noqa: S311
            price = asset.price + random_price

            AssetDaily.objects.create(asset=asset, datetime=next_date, price=price)
