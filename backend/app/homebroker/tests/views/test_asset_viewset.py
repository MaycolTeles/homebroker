"""
Module containing the tests for the Asset ViewSet.
"""

from django.urls import reverse
from rest_framework import status

from core.mixins import BaseAPITestCase
from homebroker.models import Asset
from homebroker.tests.mocks import MixerHomebrokerFactory


LIST_VIEW_NAME = "assets-list"
DETAIL_VIEW_NAME = "assets-detail"


class AssetViewSetTestCase(BaseAPITestCase):
    """
    Test case for the Asset ViewSet.

    This test case class defines all the tests for the Asset ViewSet,
    testing the CRUD operations and the filtering capabilities.
    """

    def test_should_require_authentication(self):
        """
        Assert the viewset requires authentication to access the endpoints.
        """
        url = reverse(LIST_VIEW_NAME)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_create_asset_instance(self):
        """
        Assert the viewset can create a new asset object.

        This test asserts that we can create a new asset object through the API
        using a POST method with a list URL.
        """
        self.login()

        test_name = "Test Asset"
        test_symbol = "TAS"
        test_price = 100.00
        test_image = "https://example.com/image.jpg"

        data = {
            "name": test_name,
            "symbol": test_symbol,
            "price": test_price,
            "image": test_image,
        }

        url = reverse(LIST_VIEW_NAME)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Asset.objects.count(), 1)

    def test_should_list_asset_instances(self):
        """
        Assert the viewset can list all asset objects.

        This test asserts that we can list all asset objects through the API
        using a GET method with a list URL.
        """
        self.login()

        # Creating two asset instances
        MixerHomebrokerFactory.create_asset()
        MixerHomebrokerFactory.create_asset()

        url = reverse(LIST_VIEW_NAME)
        response = self.client.get(url)

        # Asserting that the response is OK and that the count is now 2
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["count"], 2)

    def test_should_retrieve_asset_instance(self):
        """
        Assert the viewset can retrieve a single asset object.

        This test asserts that we can retrieve a single asset object through the API
        using a GET method with a detail URL.
        """
        self.login()

        test_asset = MixerHomebrokerFactory.create_asset()
        url = reverse(DETAIL_VIEW_NAME, kwargs={"pk": test_asset.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["id"], str(test_asset.id))

    def test_should_update_asset_instance(self):
        """
        Assert the viewset can update an asset object.

        This test asserts that we can update an asset object through the API
        using a PATCH method with a detail URL.
        """
        self.login()

        test_price = 100.00
        test_asset = MixerHomebrokerFactory.create_asset(price=test_price)

        self.assertEqual(test_asset.price, test_price)

        test_new_price = 200.00
        url = reverse(DETAIL_VIEW_NAME, kwargs={"pk": test_asset.id})
        response = self.client.patch(url, {"price": test_new_price})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["price"], f"{test_new_price:.2f}")

    def test_should_delete_asset_instance(self):
        """
        Assert the viewset can delete an asset object.

        This test asserts that we can delete an asset object through the API
        using a DELETE method with a detail URL.
        """
        self.login()

        test_asset = MixerHomebrokerFactory.create_asset()

        self.assertEqual(Asset.objects.count(), 1)

        url = reverse(DETAIL_VIEW_NAME, kwargs={"pk": test_asset.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Asset.objects.count(), 0)

    def test_should_filter_assets_by_price(self):
        """
        Assert the viewset filters assets by price.

        This test asserts that the viewset filters assets by price, using the following filters:
            * GREATER THAN OR EQUAL TO
            * LESS THAN OR EQUAL TO
            * RANGE
        """
        self.login()

        # Creating five asset instances
        MixerHomebrokerFactory.create_asset(price=100.00)
        MixerHomebrokerFactory.create_asset(price=200.00)
        MixerHomebrokerFactory.create_asset(price=300.00)
        MixerHomebrokerFactory.create_asset(price=400.00)
        MixerHomebrokerFactory.create_asset(price=500.00)

        url = reverse(LIST_VIEW_NAME)

        # Testing filtering by GREATER THAN OR EQUAL TO
        with self.subTest("Filtering by greater than or equal to"):
            query_filter = {"price__gte": 300.00, "ordering": "price"}
            response = self.client.get(url, query_filter)
            results = response.json()["results"]

            # Asserting that the response is OK and that the count is 3
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json()["count"], 3)
            self.assertEqual(results[0]["price"], "300.00")
            self.assertEqual(results[1]["price"], "400.00")
            self.assertEqual(results[2]["price"], "500.00")

        # Testing filtering by LESS THAN OR EQUAL TO
        with self.subTest("Filtering by less than or equal to"):
            query_filter = {"price__lte": "300.00", "ordering": "price"}
            response = self.client.get(url, query_filter)
            results = response.json()["results"]

            # Asserting that the response is OK and that the count is 3
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json()["count"], 3)
            self.assertEqual(results[0]["price"], "100.00")
            self.assertEqual(results[1]["price"], "200.00")
            self.assertEqual(results[2]["price"], "300.00")

        # Testing filtering by RANGE
        with self.subTest("Filtering by range"):
            query_filter = {"price__gt": "100.00", "price__lt": "500.00", "ordering": "price"}
            response = self.client.get(url, query_filter)
            results = response.json()["results"]

            # Asserting that the response is OK and that the count is 3
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json()["count"], 3)
            self.assertEqual(results[0]["price"], "200.00")
            self.assertEqual(results[1]["price"], "300.00")
            self.assertEqual(results[2]["price"], "400.00")

    def test_should_search_assets_by_name(self):
        """
        Assert the viewset searches assets by name.

        This test asserts that the viewset searches assets by name, using a case-insensitive search.
        """
        self.login()

        # Creating two asset instances
        MixerHomebrokerFactory.create_asset(name="APPLE")
        MixerHomebrokerFactory.create_asset(name="AMAZON")

        url = reverse(LIST_VIEW_NAME)

        # Testing searching by name
        query_filter = {"name": "APPLE"}
        response = self.client.get(url, query_filter)
        results = response.json()["results"]

        # Asserting that the response is OK and that the count is 1
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(results[0]["name"], "APPLE")

    def test_should_search_assets_by_symbol(self):
        """
        Assert the viewset searches assets by symbol.

        This test asserts that the viewset searches assets by symbol, using a case-insensitive search.
        """
        self.login()

        # Creating two asset instances
        MixerHomebrokerFactory.create_asset(symbol="APPL")
        MixerHomebrokerFactory.create_asset(symbol="AMZN")
        MixerHomebrokerFactory.create_asset(symbol="GOOGL")

        url = reverse(LIST_VIEW_NAME)

        # Testing searching by name
        query_filter = {"symbol": "GOOGL"}
        response = self.client.get(url, query_filter)
        results = response.json()["results"]

        # Asserting that the response is OK and that the count is 1
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(results[0]["symbol"], "GOOGL")
