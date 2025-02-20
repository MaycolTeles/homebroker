"""
Module containing the tests for the AssetDaily ViewSet.
"""

from django.urls import reverse
from rest_framework import status

from core.mixins import BaseAPITestCase
from core.utils import aware_datetime
from homebroker.models import AssetDaily
from homebroker.tests.mocks import MixerHomebrokerFactory


LIST_VIEW_NAME = "assets-daily-list"
DETAIL_VIEW_NAME = "assets-daily-detail"


class AssetDailyViewSetTestCase(BaseAPITestCase):
    """
    Test case for the AssetDaily ViewSet.

    This test case class defines all the tests for the AssetDaily ViewSet,
    testing the CRUD operations and the filtering capabilities.
    """

    def test_should_require_authentication(self):
        """
        Assert the viewset requires authentication to access the endpoints.
        """
        url = reverse(LIST_VIEW_NAME)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_create_asset_daily_instance(self):
        """
        Assert the viewset can create a new asset_daily object.

        This test asserts that we can create a new asset_daily object through the API
        using a POST method with a list URL.
        """
        self.login()

        test_asset = MixerHomebrokerFactory.create_asset()
        test_date = aware_datetime(2021, 1, 1)

        data = {
            "asset": test_asset.id,
            "date": test_date,
        }

        url = reverse(LIST_VIEW_NAME)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AssetDaily.objects.count(), 1)

    def test_should_list_asset_daily_instances(self):
        """
        Assert the viewset can list all asset_daily objects.

        This test asserts that we can list all asset_daily objects through the API
        using a GET method with a list URL.
        """
        self.login()

        # Creating two asset_daily instances
        MixerHomebrokerFactory.create_asset_daily()
        MixerHomebrokerFactory.create_asset_daily()

        url = reverse(LIST_VIEW_NAME)
        response = self.client.get(url)

        # Asserting that the response is OK and that the count is now 2
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["count"], 2)

    def test_should_retrieve_asset_daily_instance(self):
        """
        Assert the viewset can retrieve a single asset_daily object.

        This test asserts that we can retrieve a single asset_daily object through the API
        using a GET method with a detail URL.
        """
        self.login()

        test_asset_daily = MixerHomebrokerFactory.create_asset_daily()
        url = reverse(DETAIL_VIEW_NAME, kwargs={"pk": test_asset_daily.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["id"], str(test_asset_daily.id))

    def test_should_update_asset_daily_instance(self):
        """
        Assert the viewset can update an asset_daily object.

        This test asserts that we can update an asset_daily object through the API
        using a PATCH method with a detail URL.
        """
        self.login()

        test_date = aware_datetime(2021, 1, 1)
        test_asset_daily = MixerHomebrokerFactory.create_asset_daily(date=test_date)

        self.assertEqual(test_asset_daily.date, test_date)

        test_new_date = aware_datetime(2021, 10, 1)
        url = reverse(DETAIL_VIEW_NAME, kwargs={"pk": test_asset_daily.id})
        response = self.client.patch(url, {"date": test_new_date})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["date"], test_new_date.strftime("%Y-%m-%dT%H:%M:%SZ"))

    def test_should_delete_asset_daily_instance(self):
        """
        Assert the viewset can delete an asset_daily object.

        This test asserts that we can delete an asset_daily object through the API
        using a DELETE method with a detail URL.
        """
        self.login()

        test_asset_daily = MixerHomebrokerFactory.create_asset_daily()

        self.assertEqual(AssetDaily.objects.count(), 1)

        url = reverse(DETAIL_VIEW_NAME, kwargs={"pk": test_asset_daily.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(AssetDaily.objects.count(), 0)
