import 'package:flutter/material.dart';
import 'package:frontend/app/homebroker/api/entities/order.dart';
import 'package:frontend/app/homebroker/components/badge.dart' show BadgeLabel;
import 'package:frontend/app/homebroker/components/cards/order_card_detail.dart'
    show OrderCardDetail;
import 'package:frontend/app/homebroker/services/order_service.dart';
import 'package:frontend/config/navigation/page_navigator.dart';
import 'package:frontend/core/components/api/api_future_builder.dart';
import 'package:frontend/core/components/loading_overlay.dart';
import 'package:frontend/core/functions/platform.dart';
import 'package:frontend/core/functions/utils.dart' show getShortenedId;
import 'package:gap/gap.dart';

class OrderDetailPage extends StatefulWidget {
  static const url = '/ordens/:id';
  final String orderId;

  const OrderDetailPage({
    super.key,
    required this.orderId,
  });

  @override
  State<OrderDetailPage> createState() => _OrderDetailPageState();
}

class _OrderDetailPageState extends State<OrderDetailPage> {
  final GlobalKey<LoadingOverlayState> _loadingOverlayKey =
      GlobalKey<LoadingOverlayState>();

  @override
  Widget build(BuildContext context) {
    Widget body = _getBody();

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
      onPressed: () => PageNavigator.navigateTo(NavigationPage.assetList),
      child: const Icon(Icons.add),
    );
  }

  ListView _getBody() {
    Future<Order> order = OrderService.getOrderById(widget.orderId);

    return ListView(
      children: [
        APIFutureBuilder<Order>(
          future: order,
          errorMessage: "Erro ao carregar ordem.",
          emptyDataMessage: "Ordem inválida.",
          builder: (order) {
            return _getOrderDetail(order);
          },
        ),
      ],
    );
  }

  Column _getOrderDetail(Order order) {
    return Column(
      children: [
        const Gap(32.0),
        Padding(
          padding: const EdgeInsets.all(16.0),
          child: Text(
            "Ordem #${getShortenedId(order.id)}",
            style: TextStyle(fontSize: 24),
          ),
        ),
        const Gap(16.0),
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            BadgeLabel(
              text: order.type.name,
              backgroundColor: order.type == OrderType.BUY
                  ? Colors.green[100]!
                  : Colors.red[100]!,
              textColor: order.type == OrderType.BUY
                  ? Colors.green[800]!
                  : Colors.red[800]!,
            ),
            const Gap(8.0),
            BadgeLabel(
              text: order.status.name,
              backgroundColor:
                  _statusColor(order.status).withValues(alpha: 0.2),
              textColor: _statusColor(order.status),
            ),
          ],
        ),
        const Gap(32),
        OrderCardDetail(order: order),
        const Gap(64),
      ],
    );
  }
}

Color _statusColor(OrderStatus status) {
  switch (status) {
    case OrderStatus.OPEN:
      return Colors.blue;
    case OrderStatus.CLOSED:
      return Colors.grey;
    case OrderStatus.PENDING:
      return Colors.orange;
    case OrderStatus.FAILED:
      return Colors.red;
  }
}
