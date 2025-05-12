"""
Module containing the OrderService class.
"""

from decimal import Decimal

from django.db import transaction

from homebroker.constants import ORDER_STATUS_CHOICES, ORDER_TYPE_CHOICES
from homebroker.models import Order, WalletAsset


class OrderService:
    """
    Class containing all the business logic related to orders.
    """

    @transaction.atomic
    def execute_order(self, order: Order) -> None:
        """
        Execute the order.

        Execute the order in an atomic transaction to ensure data consistency,
        which means that if an error occurs during the process, the transaction will be rolled back
        and the data will be restored to its previous state (no operations will be saved).

        The process of executing an order is as follows:
            1. Execute the order by matching it against counterparty orders
            2. Execute the trade
            3. Update remaining shares and balances

        Args:
            order (`Order`): The order instance to be processed.
        """
        if order.status == ORDER_STATUS_CHOICES.CLOSED:
            return

        self._execute_order(order)

    def _execute_order(self, order: Order) -> None:
        """
        Execute the order.

        The process of executing an order is as follows:
            1. Execute the order by matching it against counterparty orders
            2. Execute the trade
            3. Update remaining shares and balances

        Args:
            order (`Order`): The order instance to be processed.
        """
        counterparty_orders = Order.objects.counterparty_orders(order).select_for_update()
        if not counterparty_orders:
            return

        order_remaining_shares = order.shares - order.partial
        for counterparty_order in counterparty_orders:
            # Determine the number of shares to trade
            counterparty_remaining_shares = counterparty_order.shares - counterparty_order.partial
            self.shares_to_trade = min(order_remaining_shares, counterparty_remaining_shares)

            # Determine the buyer and seller
            self._set_order_buy_and_sell(order, counterparty_order)

            # Execute the trade
            self._execute_trade()

            # Update remaining shares
            order_remaining_shares -= self.shares_to_trade
            if order_remaining_shares == 0:
                break

    def _set_order_buy_and_sell(self, order: Order, counterparty_order: Order) -> None:
        """
        Set the buyer and seller orders.

        Store the buyer and seller orders in the class attributes.
        The buyer is the order with the type "BUY" and the seller is the order with the type "SELL".

        Args:
            order (`Order`): The order that is being processed.
            counterparty_order (`Order`): The counterparty order (order with the opposite type).
        """
        if order.type == ORDER_TYPE_CHOICES.BUY:
            self.order_buy = order
            self.order_sell = counterparty_order

        else:
            self.order_buy = counterparty_order
            self.order_sell = order

    def _execute_trade(self) -> None:
        """
        Execute a trade between a BUY and a SELL order.

        A trade is executed by:
            1. Deducting the total price from the buyer's balance and adding it to the seller's balance;
            2. Increasing the partial shares of both orders;
            3. Updating the wallet assets.
        """
        # Deduct from buyer, add to seller's balances
        self._update_balances()

        # Update order partial fulfillment
        self.order_buy.increase_partial(self.shares_to_trade)
        self.order_sell.increase_partial(self.shares_to_trade)

        # Update wallets asset
        self._update_wallet_assets()

    def _update_balances(self) -> None:
        """
        Update buyer and seller balances after a trade.

        The process to update the balances is as follows:
            1. (Buyer) Deduct the total price from the user's balance and add it to their wallet.
            2. (Seller) Add the total price to the user's balance and deduct it from their wallet.
        """
        amount = Decimal(self.shares_to_trade * self.order_buy.share_price)

        self.order_buy.user.subtract_amount_from_balance(amount)
        self.order_buy.wallet.add_amount_to_balance(amount)

        self.order_sell.user.add_amount_to_balance(amount)
        self.order_sell.wallet.subtract_amount_from_balance(amount)

    def _update_wallet_assets(self) -> None:
        """
        Update the WalletAsset instances to reflect new shares.

        The process to update the WalletAsset instances is as follows:
            1. (Buyer) Add the shares to the buyer's wallet asset.
            2. (Seller) Subtract the shares from the seller's wallet asset.
        """
        wa_buy, _ = WalletAsset.objects.get_or_create(wallet=self.order_buy.wallet, asset=self.order_buy.asset)
        wa_buy.add_shares(self.shares_to_trade)

        wa_sell = WalletAsset.objects.get(wallet=self.order_sell.wallet, asset=self.order_sell.asset)
        wa_sell.subtract_shares(self.shares_to_trade)
