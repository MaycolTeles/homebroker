import 'package:flutter/material.dart';
import 'package:frontend/app/homebroker/api/entities/order.dart' show Order;
import 'package:frontend/app/homebroker/services/order_service.dart'
    show OrderService;
import 'package:frontend/config/navigation/page_navigator.dart'
    show PageNavigator, NavigationPage;
import 'package:frontend/core/components/api/api_future_builder.dart'
    show APIFutureBuilder;
import 'package:frontend/core/components/loading_overlay.dart'
    show LoadingOverlay, LoadingOverlayState;
import 'package:frontend/core/functions/platform.dart'
    show getScaffoldAccordingToPlatform;
import 'package:gap/gap.dart' show Gap;

class OrderListPage extends StatefulWidget {
  static const url = '/ordens';
  const OrderListPage({super.key});

  @override
  State<OrderListPage> createState() => _OrderListPageState();
}

class _OrderListPageState extends State<OrderListPage> {
  final GlobalKey<LoadingOverlayState> _loadingOverlayKey =
      GlobalKey<LoadingOverlayState>();

  @override
  Widget build(BuildContext context) {
    Widget body = Padding(
      padding: const EdgeInsets.all(16.0),
      child: _getBody(),
    );

    return LoadingOverlay(
      key: _loadingOverlayKey,
      scaffold: getScaffoldAccordingToPlatform(
        body: body,
        floatingActionButton: _getFloatingActionButton(),
      ),
    );
  }

  FloatingActionButton _getFloatingActionButton() {
    return FloatingActionButton(
      onPressed: () => PageNavigator.goTo(NavigationPage.assetList),
      child: const Icon(Icons.add),
    );
  }

  ListView _getBody() {
    return ListView(
      children: [
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Gap(32.0),
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: const Text(
                'Minhas Ordens',
                style: TextStyle(fontSize: 24),
              ),
            ),
            const Gap(32.0),
            getOrdersCards(),
            const Gap(32.0),
          ],
        ),
      ],
    );
  }

  APIFutureBuilder getOrdersCards() {
    Future<List<Order>> orders = OrderService.getAllOrders();

    return APIFutureBuilder(
      future: orders,
      errorMessage: "Erro ao carregar ordens.",
      emptyDataMessage: "Sem ordens no momento.",
      builder: (dynamic orders) => _buildOrdersCards(orders),
    );
  }

  ListView _buildOrdersCards(List<Order> orders) {
    List<GestureDetector> cards = [];

    for (Order order in orders) {
      cards.add(getOrderCard(order));
    }

    return ListView(
      shrinkWrap: true,
      physics: const ClampingScrollPhysics(),
      children: cards,
    );
  }

  GestureDetector getOrderCard(Order order) {
    return GestureDetector(
      onTap: () => navigateToOrderDetails(order.id),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Card(
          elevation: 10,
          clipBehavior: Clip.antiAlias,
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            child: Center(
              child: Text(
                '${order.asset.name} - ${order.type.name} - ${order.shares} - R\$${order.sharePrice.toStringAsFixed(2)}',
                style: TextStyle(color: Colors.black),
              ),
            ),
          ),
        ),
      ),
    );
  }

  navigateToOrderDetails(String orderId) {
    Map<String, String> args = {'id': orderId};
    PageNavigator.navigateTo(NavigationPage.orderDetail, arguments: args);
  }
}

void showCreateOrderModal(
  BuildContext context,
  Function rebuildWidget,
) {
  showDialog(
    context: context,
    builder: (BuildContext context) {
      return AlertDialog(
        insetPadding: const EdgeInsets.symmetric(
          horizontal: 48.0,
          vertical: 96.0,
        ),
        title: const Text("Criar Ordem"),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text("Cancelar"),
          ),
          TextButton(
            onPressed: () {
              Navigator.of(context).pop();
              rebuildWidget();
            },
            child: const Text("OK"),
          ),
        ],
      );
    },
  );
}
