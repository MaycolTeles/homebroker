"""
Module containing the tests for the Wallet ViewSet.
"""

from django.urls import reverse
from rest_framework import status

from core.mixins import BaseAPITestCase
from homebroker.models import Wallet
from homebroker.tests.mocks import MixerHomebrokerFactory


LIST_VIEW_NAME = "wallets-list"
DETAIL_VIEW_NAME = "wallets-detail"


class WalletViewSetTestCase(BaseAPITestCase):
    """
    Test case for the Wallet ViewSet.

    This test case class defines all the tests for the Wallet ViewSet,
    testing the CRUD operations and the filtering capabilities.
    """

    def test_should_require_authentication(self):
        """
        Assert the viewset requires authentication to access the endpoints.
        """
        url = reverse(LIST_VIEW_NAME)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_create_wallet_instance(self):
        """
        Assert the viewset can create a new wallet object.

        This test asserts that we can create a new wallet object through the API
        using a POST method with a list URL.
        """
        self.login()

        test_user = self.user
        test_name = "Test Wallet"

        data = {
            "user": test_user.id,
            "name": test_name,
        }

        url = reverse(LIST_VIEW_NAME)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Wallet.objects.count(), 1)

    def test_should_list_wallet_instances(self):
        """
        Assert the viewset can list all wallet objects.

        This test asserts that we can list all wallet objects through the API
        using a GET method with a list URL.
        """
        self.login()

        # Creating two wallet instances
        MixerHomebrokerFactory.create_wallet(user=self.user)
        MixerHomebrokerFactory.create_wallet(user=self.user)

        url = reverse(LIST_VIEW_NAME)
        response = self.client.get(url)

        # Asserting that the response is OK and that the count is now 2
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["count"], 2)

    def test_should_retrieve_wallet_instance(self):
        """
        Assert the viewset can retrieve a single wallet object.

        This test asserts that we can retrieve a single wallet object through the API
        using a GET method with a detail URL.
        """
        self.login()

        test_wallet = MixerHomebrokerFactory.create_wallet(user=self.user)
        url = reverse(DETAIL_VIEW_NAME, kwargs={"pk": test_wallet.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["id"], str(test_wallet.id))

    def test_should_update_wallet_instance(self):
        """
        Assert the viewset can update an wallet object.

        This test asserts that we can update an wallet object through the API
        using a PATCH method with a detail URL.
        """
        self.login()

        test_name = "Test Wallet"
        test_wallet = MixerHomebrokerFactory.create_wallet(user=self.user, name=test_name)

        self.assertEqual(test_wallet.name, test_name)

        test_new_name = "New Wallet"
        url = reverse(DETAIL_VIEW_NAME, kwargs={"pk": test_wallet.id})
        response = self.client.patch(url, {"name": test_new_name})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["name"], test_new_name)

    def test_should_delete_wallet_instance(self):
        """
        Assert the viewset can delete an wallet object.

        This test asserts that we can delete an wallet object through the API
        using a DELETE method with a detail URL.
        """
        self.login()

        test_wallet = MixerHomebrokerFactory.create_wallet(user=self.user)

        self.assertEqual(Wallet.objects.count(), 1)

        url = reverse(DETAIL_VIEW_NAME, kwargs={"pk": test_wallet.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Wallet.objects.count(), 0)

    def test_viewset_should_filter_wallets_by_user(self):
        """
        Assert the viewset filters wallets by user.

        This test asserts that the viewset filters wallets by user, only returning the wallets of the logged user.
        """
        self.login()

        # Creating two wallet instances
        MixerHomebrokerFactory.create_wallet(user=self.user)
        MixerHomebrokerFactory.create_wallet(user=self.user)

        # Creating a new user
        new_user = self.create_user()

        # Creating two wallet instances for the new user
        MixerHomebrokerFactory.create_wallet(user=new_user)
        MixerHomebrokerFactory.create_wallet(user=new_user)

        url = reverse(LIST_VIEW_NAME)
        response = self.client.get(url)

        # Asserting that the response is OK and that the count is 2
        # (only the wallets of the logged user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["count"], 2)

    def test_viewset_should_return_all_wallets_for_superuser(self):
        """
        Assert the viewset returns all wallets for superuser.

        This test asserts that the viewset returns all wallets for a superuser,
        regardless of the user who created them.
        """
        self.login()

        # Creating two wallet instances
        MixerHomebrokerFactory.create_wallet(user=self.user)
        MixerHomebrokerFactory.create_wallet(user=self.user)

        # Creating a new user
        new_user = self.create_user()

        # Creating two wallet instances for the new user
        MixerHomebrokerFactory.create_wallet(user=new_user)
        MixerHomebrokerFactory.create_wallet(user=new_user)

        # Making the logged user a superuser
        self.user.is_superuser = True
        self.user.save(update_fields=("is_superuser",))

        url = reverse(LIST_VIEW_NAME)
        response = self.client.get(url)

        # Asserting that the response is OK and that the count is 4
        # (all wallets in the database)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["count"], 4)

    def test_should_search_wallets_by_name(self):
        """
        Assert the viewset searches wallets by name.

        This test asserts that the viewset searches wallets by name, using a case-insensitive search.
        """
        self.login()

        # Creating two wallet instances
        MixerHomebrokerFactory.create_wallet(user=self.user, name="Real State")
        MixerHomebrokerFactory.create_wallet(user=self.user, name="Shares")

        url = reverse(LIST_VIEW_NAME)

        # Testing searching by name
        query_filter = {"name": "Shares"}
        response = self.client.get(url, query_filter)
        results = response.json()["results"]

        # Asserting that the response is OK and that the count is 1
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(results[0]["name"], "Shares")
