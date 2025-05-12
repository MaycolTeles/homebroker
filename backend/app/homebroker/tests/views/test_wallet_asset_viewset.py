"""
Module containing the tests for the WalletAsset ViewSet.
"""

from django.urls import reverse
from rest_framework import status

from core.mixins import BaseAPITestCase
from homebroker.models import WalletAsset
from homebroker.tests.mocks import MixerHomebrokerFactory


LIST_VIEW_NAME = "wallet-assets-list"
DETAIL_VIEW_NAME = "wallet-assets-detail"


class WalletAssetViewSetTestCase(BaseAPITestCase):
    """
    Test case for the WalletAsset ViewSet.

    This test case class defines all the tests for the WalletAsset ViewSet,
    testing the CRUD operations and the filtering capabilities.
    """

    def test_should_require_authentication(self):
        """
        Assert the viewset requires authentication to access the endpoints.
        """
        url = reverse(LIST_VIEW_NAME)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_create_wallet_asset_instance(self):
        """
        Assert the viewset can create a new wallet_asset object.

        This test asserts that we can create a new wallet_asset object through the API
        using a POST method with a list URL.
        """
        self.login()

        test_shares = 100.00
        test_wallet = MixerHomebrokerFactory.create_wallet()
        test_asset = MixerHomebrokerFactory.create_asset()

        data = {
            "wallet": test_wallet.id,
            "asset": test_asset.id,
            "shares": test_shares,
        }

        url = reverse(LIST_VIEW_NAME)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WalletAsset.objects.count(), 1)

    def test_should_list_wallet_asset_instances(self):
        """
        Assert the viewset can list all wallet_asset objects.

        This test asserts that we can list all wallet_asset objects through the API
        using a GET method with a list URL.
        """
        self.login()

        # Creating two wallet_asset instances
        MixerHomebrokerFactory.create_wallet_asset()
        MixerHomebrokerFactory.create_wallet_asset()

        url = reverse(LIST_VIEW_NAME)
        response = self.client.get(url)

        # Asserting that the response is OK and that the count is now 2
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["count"], 2)

    def test_should_retrieve_wallet_asset_instance(self):
        """
        Assert the viewset can retrieve a single wallet_asset object.

        This test asserts that we can retrieve a single wallet_asset object through the API
        using a GET method with a detail URL.
        """
        self.login()

        test_wallet_asset = MixerHomebrokerFactory.create_wallet_asset()
        url = reverse(DETAIL_VIEW_NAME, kwargs={"pk": test_wallet_asset.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["id"], str(test_wallet_asset.id))

    def test_should_update_wallet_asset_instance(self):
        """
        Assert the viewset can update an wallet_asset object.

        This test asserts that we can update an wallet_asset object through the API
        using a PATCH method with a detail URL.
        """
        self.login()

        test_shares = 100
        test_wallet_asset = MixerHomebrokerFactory.create_wallet_asset(shares=test_shares)

        self.assertEqual(test_wallet_asset.shares, test_shares)

        test_new_shares = 200
        url = reverse(DETAIL_VIEW_NAME, kwargs={"pk": test_wallet_asset.id})
        response = self.client.patch(url, {"shares": test_new_shares})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["shares"], test_new_shares)

    def test_should_delete_wallet_asset_instance(self):
        """
        Assert the viewset can delete an wallet_asset object.

        This test asserts that we can delete an wallet_asset object through the API
        using a DELETE method with a detail URL.
        """
        self.login()

        test_wallet_asset = MixerHomebrokerFactory.create_wallet_asset()

        self.assertEqual(WalletAsset.objects.count(), 1)

        url = reverse(DETAIL_VIEW_NAME, kwargs={"pk": test_wallet_asset.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(WalletAsset.objects.count(), 0)
