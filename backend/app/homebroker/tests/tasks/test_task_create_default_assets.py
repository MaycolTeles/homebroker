"""
Module containing the tests for the `task_create_default_assets` task.
"""

from core.mixins import BaseTestCase
from homebroker.models import Asset
from homebroker.tasks import task_create_default_assets
from homebroker.tasks.task_create_default_assets import ASSETS


class TaskCreateDefaultAssetsTestCase(BaseTestCase):
    """
    Class to test the task_create_default_assets task.
    """

    def test_should_create_default_assets(self):
        """
        Assert the task creates all the default assets.
        """
        # Ensure there are no assets previously
        assets = Asset.objects.all()

        self.assertEqual(assets.count(), 0)

        # Call the task to create the default assets.
        task_create_default_assets()

        # Ensure that all assets were created.
        assets = Asset.objects.all()

        self.assertEqual(assets.count(), len(ASSETS))
