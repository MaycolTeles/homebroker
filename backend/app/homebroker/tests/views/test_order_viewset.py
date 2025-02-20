"""
Module containing the tests for the Order ViewSet.
"""

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

    def test_should_create_order_instance(self):
        """
        Assert the viewset can create a new order object.

        This test asserts that we can create a new order object through the API
        using a POST method with a list URL.
        """
        self.login()

        test_user = self.user
        test_asset = MixerHomebrokerFactory.create_asset()
        test_shares = 100.0
        test_partial = 50.0
        test_price = 10.0

        data = {
            "user": test_user.id,
            "asset": test_asset.id,
            "shares": test_shares,
            "partial": test_partial,
            "price": test_price,
            "status": ORDER_STATUS_CHOICES.OPEN,
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

    def test_should_update_order_instance(self):
        """
        Assert the viewset can update an order object.

        This test asserts that we can update an order object through the API
        using a PATCH method with a detail URL.
        """
        self.login()

        test_shares = 100.0
        test_partial = 50.0
        test_price = 10.0
        test_order = MixerHomebrokerFactory.create_order(
            user=self.user,
            shares=test_shares,
            partial=test_partial,
            price=test_price,
        )

        self.assertEqual(test_order.shares, test_shares)
        self.assertEqual(test_order.partial, test_partial)
        self.assertEqual(test_order.price, test_price)

        test_new_shares = 200.0
        test_new_partial = 100.0
        test_new_price = 20.0

        data = {
            "shares": test_new_shares,
            "partial": test_new_partial,
            "price": test_new_price,
        }
        url = reverse(DETAIL_VIEW_NAME, kwargs={"pk": test_order.id})
        response = self.client.patch(url, data)
        r = response.json()

        actual_shares = r["shares"]
        actual_partial = r["partial"]
        actual_price = r["price"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(actual_shares, f"{test_new_shares:.2f}")
        self.assertEqual(actual_partial, test_new_partial)
        self.assertEqual(actual_price, f"{test_new_price:.2f}")

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
        self.user.save()

        url = reverse(LIST_VIEW_NAME)
        response = self.client.get(url)

        # Asserting that the response is OK and that the count is 4
        # (all orders in the database)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["count"], 4)
