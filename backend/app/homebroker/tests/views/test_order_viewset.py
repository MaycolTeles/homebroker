"""
Module containing the tests for the Order ViewSet.
"""

from decimal import Decimal

from django.test import override_settings
from django.urls import reverse
from rest_framework import status

from core.mixins import BaseAPITestCase
from homebroker.constants import ORDER_STATUS_CHOICES, ORDER_TYPE_CHOICES
from homebroker.models import Order
from homebroker.tests.mocks import MixerHomebrokerFactory


LIST_VIEW_NAME = "orders-list"
DETAIL_VIEW_NAME = "orders-detail"


class OrderViewSetTestCase(BaseAPITestCase):
    """
    Test case for the Order ViewSet.

    This test case class defines all the tests for the Order ViewSet,
    testing the CRUD operations and the filtering capabilities.
    """

    def test_should_require_authentication(self):
        """
        Assert the viewset requires authentication to access the endpoints.
        """
        url = reverse(LIST_VIEW_NAME)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True, CELERY_TASK_EAGER_PROPAGATES=True)
    def test_should_create_order_instance(self):
        """
        Assert the viewset can create a new order object.

        This test asserts that we can create a new order object through the API
        using a POST method with a list URL.
        """
        self.login()
        self.user.add_amount_to_balance(Decimal(100_000))

        test_asset = MixerHomebrokerFactory.create_asset()
        test_wallet = MixerHomebrokerFactory.create_wallet()
        test_shares = 100.0
        test_partial = 50.0
        test_share_price = 10.0

        data = {
            "asset": test_asset.id,
            "wallet": test_wallet.id,
            "shares": test_shares,
            "partial": test_partial,
            "share_price": test_share_price,
            "type": ORDER_TYPE_CHOICES.BUY,
        }

        url = reverse(LIST_VIEW_NAME)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)

    def test_should_list_order_instances(self):
        """
        Assert the viewset can list all order objects.

        This test asserts that we can list all order objects through the API
        using a GET method with a list URL.
        """
        self.login()

        # Creating two order instances
        MixerHomebrokerFactory.create_order(user=self.user)
        MixerHomebrokerFactory.create_order(user=self.user)

        url = reverse(LIST_VIEW_NAME)
        response = self.client.get(url)

        # Asserting that the response is OK and that the count is now 2
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["count"], 2)

    def test_should_retrieve_order_instance(self):
        """
        Assert the viewset can retrieve a single order object.

        This test asserts that we can retrieve a single order object through the API
        using a GET method with a detail URL.
        """
        self.login()

        test_order = MixerHomebrokerFactory.create_order(user=self.user)
        url = reverse(DETAIL_VIEW_NAME, kwargs={"pk": test_order.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["id"], str(test_order.id))

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True, CELERY_TASK_EAGER_PROPAGATES=True)
    def test_should_update_order_instance(self):
        """
        Assert the viewset can update an order object.

        This test asserts that we can update an order object through the API
        using a PATCH method with a detail URL.
        """
        self.login()
        self.user.add_amount_to_balance(Decimal(100_000))

        test_order = MixerHomebrokerFactory.create_order(
            user=self.user,
            total_price=300,
            type=ORDER_TYPE_CHOICES.BUY,
        )

        test_new_share_price = 20
        test_new_shares = 200
        test_new_total_price = test_new_shares * test_new_share_price

        data = {
            "shares": test_new_shares,
            "share_price": test_new_share_price,
        }
        url = reverse(DETAIL_VIEW_NAME, kwargs={"pk": test_order.id})
        response = self.client.patch(url, data)
        r = response.json()

        actual_shares = r["shares"]
        actual_share_price = r["share_price"]
        actual_total_price = r["total_price"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(actual_shares, test_new_shares)
        self.assertEqual(actual_share_price, f"{test_new_share_price:.2f}")
        self.assertEqual(actual_total_price, f"{test_new_total_price:.2f}")

    def test_should_delete_order_instance(self):
        """
        Assert the viewset can delete an order object.

        This test asserts that we can delete an order object through the API
        using a DELETE method with a detail URL.
        """
        self.login()

        test_order = MixerHomebrokerFactory.create_order(user=self.user)

        self.assertEqual(Order.objects.count(), 1)

        url = reverse(DETAIL_VIEW_NAME, kwargs={"pk": test_order.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 0)

    def test_viewset_should_filter_orders_by_user(self):
        """
        Assert the viewset filters orders by user.

        This test asserts that the viewset filters orders by user, only returning the orders of the logged user.
        """
        self.login()

        # Creating two order instances
        MixerHomebrokerFactory.create_order(user=self.user)
        MixerHomebrokerFactory.create_order(user=self.user)

        # Creating a new user
        new_user = self.create_user()

        # Creating two order instances for the new user
        MixerHomebrokerFactory.create_order(user=new_user)
        MixerHomebrokerFactory.create_order(user=new_user)

        url = reverse(LIST_VIEW_NAME)
        response = self.client.get(url)

        # Asserting that the response is OK and that the count is 2
        # (only the orders of the logged user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["count"], 2)

    def test_viewset_should_return_all_orders_for_superuser(self):
        """
        Assert the viewset returns all orders for superuser.

        This test asserts that the viewset returns all orders for a superuser,
        regardless of the user who created them.
        """
        self.login()

        # Creating two order instances
        MixerHomebrokerFactory.create_order(user=self.user)
        MixerHomebrokerFactory.create_order(user=self.user)

        # Creating a new user
        new_user = self.create_user()

        # Creating two order instances for the new user
        MixerHomebrokerFactory.create_order(user=new_user)
        MixerHomebrokerFactory.create_order(user=new_user)

        # Making the logged user a superuser
        self.user.is_superuser = True
        self.user.save(update_fields=("is_superuser",))

        url = reverse(LIST_VIEW_NAME)
        response = self.client.get(url)

        # Asserting that the response is OK and that the count is 4
        # (all orders in the database)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["count"], 4)

    def test_should_filter_orders_by_shares(self):
        """
        Assert the viewset filters orders by shares.

        This test asserts that the viewset filters orders by shares, using the following filters:
            * GREATER THAN OR EQUAL TO
            * LESS THAN OR EQUAL TO
            * RANGE
        """
        self.login()

        # Creating five order instances
        MixerHomebrokerFactory.create_order(user=self.user, shares=100)
        MixerHomebrokerFactory.create_order(user=self.user, shares=200)
        MixerHomebrokerFactory.create_order(user=self.user, shares=300)
        MixerHomebrokerFactory.create_order(user=self.user, shares=400)
        MixerHomebrokerFactory.create_order(user=self.user, shares=500)

        url = reverse(LIST_VIEW_NAME)

        # Testing filtering by GREATER THAN OR EQUAL TO
        with self.subTest("Filtering by greater than or equal to"):
            query_filter = {"shares__gte": 300, "ordering": "shares"}
            response = self.client.get(url, query_filter)
            results = response.json()["results"]

            # Asserting that the response is OK and that the count is 3
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json()["count"], 3)
            self.assertEqual(results[0]["shares"], 300)
            self.assertEqual(results[1]["shares"], 400)
            self.assertEqual(results[2]["shares"], 500)

        # Testing filtering by LESS THAN OR EQUAL TO
        with self.subTest("Filtering by less than or equal to"):
            query_filter = {"shares__lte": "300", "ordering": "shares"}
            response = self.client.get(url, query_filter)
            results = response.json()["results"]

            # Asserting that the response is OK and that the count is 3
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json()["count"], 3)
            self.assertEqual(results[0]["shares"], 100)
            self.assertEqual(results[1]["shares"], 200)
            self.assertEqual(results[2]["shares"], 300)

        # Testing filtering by RANGE
        with self.subTest("Filtering by range"):
            query_filter = {"shares__gt": "100", "shares__lt": "500", "ordering": "shares"}
            response = self.client.get(url, query_filter)
            results = response.json()["results"]

            # Asserting that the response is OK and that the count is 3
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json()["count"], 3)
            self.assertEqual(results[0]["shares"], 200)
            self.assertEqual(results[1]["shares"], 300)
            self.assertEqual(results[2]["shares"], 400)

    def test_should_filter_orders_by_share_price(self):
        """
        Assert the viewset filters orders by share_price.

        This test asserts that the viewset filters orders by share_price, using the following filters:
            * GREATER THAN OR EQUAL TO
            * LESS THAN OR EQUAL TO
            * RANGE
        """
        self.login()

        # Creating five order instances
        MixerHomebrokerFactory.create_order(user=self.user, share_price=10.00)
        MixerHomebrokerFactory.create_order(user=self.user, share_price=20.00)
        MixerHomebrokerFactory.create_order(user=self.user, share_price=30.00)
        MixerHomebrokerFactory.create_order(user=self.user, share_price=40.00)
        MixerHomebrokerFactory.create_order(user=self.user, share_price=50.00)

        url = reverse(LIST_VIEW_NAME)

        # Testing filtering by GREATER THAN OR EQUAL TO
        with self.subTest("Filtering by greater than or equal to"):
            query_filter = {"share_price__gte": 30.00, "ordering": "share_price"}
            response = self.client.get(url, query_filter)
            results = response.json()["results"]

            # Asserting that the response is OK and that the count is 3
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json()["count"], 3)
            self.assertEqual(results[0]["share_price"], "30.00")
            self.assertEqual(results[1]["share_price"], "40.00")
            self.assertEqual(results[2]["share_price"], "50.00")

        # Testing filtering by LESS THAN OR EQUAL TO
        with self.subTest("Filtering by less than or equal to"):
            query_filter = {"share_price__lte": "30.00", "ordering": "share_price"}
            response = self.client.get(url, query_filter)
            results = response.json()["results"]

            # Asserting that the response is OK and that the count is 3
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json()["count"], 3)
            self.assertEqual(results[0]["share_price"], "10.00")
            self.assertEqual(results[1]["share_price"], "20.00")
            self.assertEqual(results[2]["share_price"], "30.00")

        # Testing filtering by RANGE
        with self.subTest("Filtering by range"):
            query_filter = {"share_price__gt": "10.00", "share_price__lt": "50.00", "ordering": "share_price"}
            response = self.client.get(url, query_filter)
            results = response.json()["results"]

            # Asserting that the response is OK and that the count is 3
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json()["count"], 3)
            self.assertEqual(results[0]["share_price"], "20.00")
            self.assertEqual(results[1]["share_price"], "30.00")
            self.assertEqual(results[2]["share_price"], "40.00")

    def test_should_filter_orders_by_status(self):
        """
        Assert the viewset filters orders by status.

        This test asserts that the viewset filters orders by status, using the following filters:
            * CLOSED
            * FAILED
            * OPEN
        """
        self.login()

        # Creating five order instances
        MixerHomebrokerFactory.create_order(user=self.user, status=ORDER_STATUS_CHOICES.CLOSED)
        MixerHomebrokerFactory.create_order(user=self.user, status=ORDER_STATUS_CHOICES.CLOSED)
        MixerHomebrokerFactory.create_order(user=self.user, status=ORDER_STATUS_CHOICES.OPEN)
        MixerHomebrokerFactory.create_order(user=self.user, status=ORDER_STATUS_CHOICES.OPEN)
        MixerHomebrokerFactory.create_order(user=self.user, status=ORDER_STATUS_CHOICES.FAILED)

        url = reverse(LIST_VIEW_NAME)

        # Testing filtering by STATUS == CLOSED
        with self.subTest("Filtering by status closed"):
            query_filter = {"status": ORDER_STATUS_CHOICES.CLOSED}
            response = self.client.get(url, query_filter)

            # Asserting that the response is OK and that the count is 2
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json()["count"], 2)

        # Testing filtering by STATUS == OPEN
        with self.subTest("Filtering by status open"):
            query_filter = {"status": ORDER_STATUS_CHOICES.OPEN}
            response = self.client.get(url, query_filter)

            # Asserting that the response is OK and that the count is 2
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json()["count"], 2)

        # Testing filtering by STATUS == FAILED
        with self.subTest("Filtering by status failed"):
            query_filter = {"status": ORDER_STATUS_CHOICES.FAILED}
            response = self.client.get(url, query_filter)

            # Asserting that the response is OK and that the count is 1
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json()["count"], 1)

    def test_should_filter_orders_by_type(self):
        """
        Assert the viewset filters orders by type.

        This test asserts that the viewset filters orders by type, using the following filters:
            * BUY
            * SELL
        """
        self.login()

        # Creating five order instances
        MixerHomebrokerFactory.create_order(user=self.user, type=ORDER_TYPE_CHOICES.BUY)
        MixerHomebrokerFactory.create_order(user=self.user, type=ORDER_TYPE_CHOICES.BUY)
        MixerHomebrokerFactory.create_order(user=self.user, type=ORDER_TYPE_CHOICES.BUY)
        MixerHomebrokerFactory.create_order(user=self.user, type=ORDER_TYPE_CHOICES.SELL)
        MixerHomebrokerFactory.create_order(user=self.user, type=ORDER_TYPE_CHOICES.SELL)

        url = reverse(LIST_VIEW_NAME)

        # Testing filtering by TYPE == BUY
        with self.subTest("Filtering by type buy"):
            query_filter = {"type": ORDER_TYPE_CHOICES.BUY}
            response = self.client.get(url, query_filter)

            # Asserting that the response is OK and that the count is 3
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json()["count"], 3)

        # Testing filtering by TYPE == SELL
        with self.subTest("Filtering by type sell"):
            query_filter = {"type": ORDER_TYPE_CHOICES.SELL}
            response = self.client.get(url, query_filter)

            # Asserting that the response is OK and that the count is 2
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json()["count"], 2)

    def test_should_search_orders_by_asset_id(self):
        """
        Assert the viewset searches orders by the asset id.

        This test asserts that the viewset searches orders by the asset id.
        """
        self.login()

        # Creating two order instances
        asset_one = MixerHomebrokerFactory.create_asset()
        asset_two = MixerHomebrokerFactory.create_asset()

        MixerHomebrokerFactory.create_order(user=self.user, asset=asset_one)
        MixerHomebrokerFactory.create_order(user=self.user, asset=asset_two)

        url = reverse(LIST_VIEW_NAME)

        # Testing searching by name
        query_filter = {"asset": asset_one.id}
        response = self.client.get(url, query_filter)
        results = response.json()["results"]

        # Asserting that the response is OK and that the count is 1
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(results[0]["asset"]["id"], str(asset_one.id))
