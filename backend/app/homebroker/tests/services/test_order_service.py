"""
Module containing the tests for the `OrderService` service class.
"""

from typing import Any

from django.db.models import Model

from core.mixins import BaseTransactionTestCase
from homebroker.constants import ORDER_STATUS_CHOICES, ORDER_TYPE_CHOICES
from homebroker.models import Order
from homebroker.services import OrderService
from homebroker.tests.mocks import MixerHomebrokerFactory


class OrderServiceTestCase(BaseTransactionTestCase):
    """
    Class to test the OrderService service class.
    """

    def setUp(self) -> None:
        """
        Set up default test data for each test case.
        """
        self.test_user_current_balance = 10_000
        self.test_asset = MixerHomebrokerFactory.create_asset()
        self.test_number_of_shares = 10
        self.test_share_price = 100
        self.test_total_price = self.test_number_of_shares * self.test_share_price
        self.created_instances: list[Model] = []

        return super().setUp()

    def _get_default_order_data(self) -> dict[str, Any]:
        return {
            "asset": self.test_asset,
            "shares": self.test_number_of_shares,
            "share_price": self.test_share_price,
            "total_price": self.test_total_price,
        }

    def _create_buy_orders(self, orders_data: tuple[dict[str, Any], ...]) -> list[Order]:
        user = self.create_user(current_balance=self.test_user_current_balance)
        wallet = MixerHomebrokerFactory.create_wallet(user=user)
        orders = []

        for order_data in orders_data:
            order = MixerHomebrokerFactory.create_order(
                user=user,
                wallet=wallet,
                type=ORDER_TYPE_CHOICES.BUY,
                **order_data,
            )
            orders.append(order)

        self.created_instances.extend((user, wallet, *orders))
        return orders

    def _create_sell_orders(self, orders_data: tuple[dict[str, Any], ...]) -> list[Order]:
        user = self.create_user(current_balance=self.test_user_current_balance)
        wallet = MixerHomebrokerFactory.create_wallet(
            user=user, total_invested=self.test_total_price, current_balance=self.test_total_price
        )
        MixerHomebrokerFactory.create_wallet_asset(
            wallet=wallet, asset=self.test_asset, shares=self.test_number_of_shares
        )

        orders = []
        for order_data in orders_data:
            order = MixerHomebrokerFactory.create_order(
                user=user,
                wallet=wallet,
                type=ORDER_TYPE_CHOICES.SELL,
                **order_data,
            )
            orders.append(order)

        self.created_instances.extend((user, wallet, *orders))
        return orders

    def _refresh_all_from_db(self) -> None:
        for instance in self.created_instances:
            instance.refresh_from_db()

    def test_should_execute_buy_order_trade_using_single_counterparty_order(self) -> None:
        """
        Assert that a new buy order is processed correctly by using a single counterparty order.
        """
        # Create the test data
        order_buy_data = self._get_default_order_data()
        order_buy = self._create_buy_orders((order_buy_data,))[0]

        order_counterparty_data = self._get_default_order_data()
        order_counterparty = self._create_sell_orders((order_counterparty_data,))[0]

        # Execute the test
        OrderService().execute_order(order_buy)
        self._refresh_all_from_db()

        # Check the results
        with self.subTest("Buy order processed correctly"):
            user_buy = order_buy.user
            wallet_buy = order_buy.wallet
            new_buy_user_current_balance = self.test_user_current_balance - self.test_total_price

            self.assertEqual(order_buy.partial, self.test_number_of_shares)
            self.assertEqual(order_buy.status, ORDER_STATUS_CHOICES.CLOSED)
            self.assertEqual(user_buy.current_balance, new_buy_user_current_balance)
            self.assertEqual(wallet_buy.total_invested, self.test_total_price)
            self.assertEqual(wallet_buy.current_balance, self.test_total_price)
            self.assertEqual(wallet_buy.assets.get(asset=self.test_asset).shares, self.test_number_of_shares)

        with self.subTest("Counterparty order processed correctly"):
            user_counterparty = order_counterparty.user
            wallet_counterparty = order_counterparty.wallet
            new_counterparty_user_current_balance = self.test_user_current_balance + self.test_total_price

            self.assertEqual(order_counterparty.partial, self.test_number_of_shares)
            self.assertEqual(order_counterparty.status, ORDER_STATUS_CHOICES.CLOSED)
            self.assertEqual(user_counterparty.current_balance, new_counterparty_user_current_balance)
            self.assertEqual(wallet_counterparty.total_invested, 0)
            self.assertEqual(wallet_counterparty.current_balance, 0)
            self.assertEqual(wallet_counterparty.assets.get(asset=self.test_asset).shares, 0)

    def test_should_execute_buy_order_trade_using_multiple_counterparty_orders(self) -> None:
        """
        Assert that a new buy order is processed correctly by using multiple counterparty orders to fulfill it.
        """
        # Create the test data
        ## Create order with 10 shares
        order_buy_data = self._get_default_order_data()
        order_buy = self._create_buy_orders((order_buy_data,))[0]

        ## Set first counterparty order shares to only 5
        test_order_counterparty_1_number_of_shares = 5
        order_counterparty_data_1 = self._get_default_order_data()
        order_counterparty_data_1["shares"] = test_order_counterparty_1_number_of_shares

        ## Set second counterparty order shares to only 4
        test_order_counterparty_2_number_of_shares = 4
        order_counterparty_data_2 = self._get_default_order_data()
        order_counterparty_data_2["shares"] = test_order_counterparty_2_number_of_shares

        ## Set third counterparty order shares to only 3
        test_order_counterparty_3_number_of_shares = 3
        order_counterparty_data_3 = self._get_default_order_data()
        order_counterparty_data_3["shares"] = test_order_counterparty_3_number_of_shares

        ## Create all counterparty orders
        order_counterparty_data = (order_counterparty_data_1, order_counterparty_data_2, order_counterparty_data_3)
        counterparty_orders = self._create_sell_orders(order_counterparty_data)
        order_counterparty_1, order_counterparty_2, order_counterparty_3 = counterparty_orders

        # Execute the test
        OrderService().execute_order(order_buy)
        self._refresh_all_from_db()

        # Check the results
        with self.subTest("Buy order processed correctly"):
            user_buy = order_buy.user
            wallet_buy = order_buy.wallet
            new_buy_user_current_balance = self.test_user_current_balance - self.test_total_price

            self.assertEqual(order_buy.partial, self.test_number_of_shares)
            self.assertEqual(order_buy.status, ORDER_STATUS_CHOICES.CLOSED)
            self.assertEqual(user_buy.current_balance, new_buy_user_current_balance)
            self.assertEqual(wallet_buy.total_invested, self.test_total_price)
            self.assertEqual(wallet_buy.current_balance, self.test_total_price)
            self.assertEqual(wallet_buy.assets.get(asset=self.test_asset).shares, self.test_number_of_shares)

        with self.subTest("Counterparty order 1 processed correctly - Order Fulfilled"):
            self.assertEqual(order_counterparty_1.partial, test_order_counterparty_1_number_of_shares)
            self.assertEqual(order_counterparty_1.status, ORDER_STATUS_CHOICES.CLOSED)

        with self.subTest("Counterparty order 2 processed correctly - Order Fulfilled"):
            self.assertEqual(order_counterparty_2.partial, test_order_counterparty_2_number_of_shares)
            self.assertEqual(order_counterparty_2.status, ORDER_STATUS_CHOICES.CLOSED)

        with self.subTest("Counterparty order 3 processed correctly - Order Partially Processed"):
            counterparty_shares = order_counterparty_1.shares + order_counterparty_2.shares
            number_of_shares_partially_processed = order_buy.shares - counterparty_shares

            self.assertEqual(order_counterparty_3.partial, number_of_shares_partially_processed)
            self.assertEqual(order_counterparty_3.status, ORDER_STATUS_CHOICES.OPEN)

        with self.subTest("All counterparty orders processed correctly"):
            user_counterparty = order_counterparty_1.user
            wallet_counterparty = order_counterparty_1.wallet
            new_counterparty_user_current_balance = self.test_user_current_balance + self.test_total_price

            self.assertEqual(user_counterparty.current_balance, new_counterparty_user_current_balance)
            self.assertEqual(wallet_counterparty.total_invested, 0)
            self.assertEqual(wallet_counterparty.current_balance, 0)
            self.assertEqual(wallet_counterparty.assets.get(asset=self.test_asset).shares, 0)

    def test_should_execute_sell_order_trade_using_single_counterparty_order(self) -> None:
        """
        Assert that a new sell order is processed correctly by using a single counterparty order.
        """
        # Create the test data
        order_sell_data = self._get_default_order_data()
        order_sell = self._create_sell_orders((order_sell_data,))[0]

        order_counterparty_data = self._get_default_order_data()
        order_counterparty = self._create_buy_orders((order_counterparty_data,))[0]

        # Execute the test
        OrderService().execute_order(order_sell)
        self._refresh_all_from_db()

        # Check the results
        with self.subTest("Sell order processed correctly"):
            user_sell = order_sell.user
            wallet_sell = order_sell.wallet
            new_sell_user_current_balance = self.test_user_current_balance + self.test_total_price

            self.assertEqual(order_sell.partial, self.test_number_of_shares)
            self.assertEqual(order_sell.status, ORDER_STATUS_CHOICES.CLOSED)
            self.assertEqual(user_sell.current_balance, new_sell_user_current_balance)
            self.assertEqual(wallet_sell.total_invested, 0)
            self.assertEqual(wallet_sell.current_balance, 0)
            self.assertEqual(wallet_sell.assets.get(asset=self.test_asset).shares, 0)

        with self.subTest("Counterparty order processed correctly"):
            user_counterparty = order_counterparty.user
            wallet_counterparty = order_counterparty.wallet
            new_counterparty_user_current_balance = self.test_user_current_balance - self.test_total_price

            self.assertEqual(order_counterparty.partial, self.test_number_of_shares)
            self.assertEqual(order_counterparty.status, ORDER_STATUS_CHOICES.CLOSED)
            self.assertEqual(user_counterparty.current_balance, new_counterparty_user_current_balance)
            self.assertEqual(wallet_counterparty.total_invested, self.test_total_price)
            self.assertEqual(wallet_counterparty.current_balance, self.test_total_price)
            self.assertEqual(wallet_counterparty.assets.get(asset=self.test_asset).shares, self.test_number_of_shares)

    def test_should_execute_sell_order_trade_using_multiple_counterparty_orders(self) -> None:
        """
        Assert a new sell order is processed correctly by using multiple counterparty orders to fulfill it.
        """
        # Create the test data
        ## Create order with 10 shares
        order_sell_data = self._get_default_order_data()
        order_sell = self._create_sell_orders((order_sell_data,))[0]

        ## Set first counterparty order shares to only 7
        test_order_counterparty_1_number_of_shares = 7
        order_counterparty_data_1 = self._get_default_order_data()
        order_counterparty_data_1["shares"] = test_order_counterparty_1_number_of_shares

        ## Set second counterparty order shares to only 5
        test_order_counterparty_2_number_of_shares = 5
        order_counterparty_data_2 = self._get_default_order_data()
        order_counterparty_data_2["shares"] = test_order_counterparty_2_number_of_shares

        ## Set third counterparty order shares to only 3
        test_order_counterparty_3_number_of_shares = 3
        order_counterparty_data_3 = self._get_default_order_data()
        order_counterparty_data_3["shares"] = test_order_counterparty_3_number_of_shares

        ## Create all counterparty orders
        order_counterparty_data = (order_counterparty_data_1, order_counterparty_data_2, order_counterparty_data_3)
        counterparty_orders = self._create_buy_orders(order_counterparty_data)
        order_counterparty_1, order_counterparty_2, order_counterparty_3 = counterparty_orders

        # Execute the test
        OrderService().execute_order(order_sell)
        self._refresh_all_from_db()

        # Check the results
        with self.subTest("Sell order processed correctly"):
            user_sell = order_sell.user
            wallet_sell = order_sell.wallet
            new_sell_user_current_balance = self.test_user_current_balance + self.test_total_price

            self.assertEqual(order_sell.partial, self.test_number_of_shares)
            self.assertEqual(order_sell.status, ORDER_STATUS_CHOICES.CLOSED)
            self.assertEqual(user_sell.current_balance, new_sell_user_current_balance)
            self.assertEqual(wallet_sell.total_invested, 0)
            self.assertEqual(wallet_sell.current_balance, 0)
            self.assertEqual(wallet_sell.assets.get(asset=self.test_asset).shares, 0)

        with self.subTest("Counterparty order 1 processed correctly - Order Fulfilled"):
            self.assertEqual(order_counterparty_1.partial, test_order_counterparty_1_number_of_shares)
            self.assertEqual(order_counterparty_1.status, ORDER_STATUS_CHOICES.CLOSED)

        with self.subTest("Counterparty order 2 processed correctly - Order Partially Processed"):
            remaining_shares_to_process = order_sell.shares - order_counterparty_1.shares

            self.assertEqual(order_counterparty_2.partial, remaining_shares_to_process)
            self.assertEqual(order_counterparty_2.status, ORDER_STATUS_CHOICES.OPEN)

        with self.subTest("Counterparty order 3 processed correctly - Order Not Processed At All"):
            self.assertEqual(order_counterparty_3.partial, 0)
            self.assertEqual(order_counterparty_3.status, ORDER_STATUS_CHOICES.OPEN)

        with self.subTest("Counterparty orders processed correctly"):
            user_counterparty = order_counterparty_1.user
            wallet_counterparty = order_counterparty_1.wallet
            new_counterparty_user_current_balance = self.test_user_current_balance - self.test_total_price

            self.assertEqual(user_counterparty.current_balance, new_counterparty_user_current_balance)
            self.assertEqual(wallet_counterparty.total_invested, self.test_total_price)
            self.assertEqual(wallet_counterparty.current_balance, self.test_total_price)
            self.assertEqual(wallet_counterparty.assets.get(asset=self.test_asset).shares, self.test_number_of_shares)
