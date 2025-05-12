"""
Module containing the tests for the `task_create_default_assets_dailies` task.
"""

from core.mixins import BaseTestCase
from homebroker.models import AssetDaily
from homebroker.tasks import task_create_default_assets, task_create_default_assets_dailies


class TaskCreateDefaultAssetsDailiesTestCase(BaseTestCase):
    """
    Class to test the task_create_default_assets_dailies task.
    """

    def test_should_create_default_assets_dailies(self):
        """
        Assert the task creates all the default assets.
        """
        # Ensure there are no assets dailies previously
        assets_dailies = AssetDaily.objects.all()

        self.assertEqual(assets_dailies.count(), 0)

        # Ensure there're assets created already.
        task_create_default_assets()

        # Call the task to create the default assets dailies.
        task_create_default_assets_dailies()

        # Ensure that all assets dailies were created.
        assets_dailies = AssetDaily.objects.all()

        self.assertEqual(assets_dailies.count(), 40)
