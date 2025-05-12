import 'package:frontend/app/homebroker/api/entities/order.dart'
    show Order, OrderType;
import 'package:frontend/config/api/api.dart';
import 'package:frontend/config/api/paginated_response.dart';

class OrderDTO {
  final String assetId;
  final String walletId;
  final int shares;
  final double sharePrice;
  final OrderType type;

  OrderDTO({
    required this.assetId,
    required this.walletId,
    required this.shares,
    required this.sharePrice,
    required this.type,
  });

  Map<String, String> toJson() {
    return {
      'asset': assetId,
      'wallet': walletId,
      'shares': shares.toString(),
      'share_price': sharePrice.toString(),
      'type': type.name,
    };
  }
}

class OrderAPI {
  static const String _ordersEndpoint = 'orders';

  static Future<List<Order>> getAllOrders() async {
    final response = await API.get(_ordersEndpoint);
    final paginatedResponse = PaginatedResponse.fromJson(
      response.data,
      (json) => Order.fromJson(json),
    );

    return paginatedResponse.results;
  }

  static Future<Order> getOrderById(String orderId) async {
    final response = await API.get('$_ordersEndpoint/$orderId');
    Order order = Order.fromJson(response.data);

    return order;
  }

  static Future<Order> createOrder(OrderDTO dto) async {
    final body = dto.toJson();
    final response = await API.post(_ordersEndpoint, body: body);
    Order order = Order.fromJson(response.data);

    return order;
  }

  static Future<void> deleteOrder(String orderId) async {
    final response = await API.delete('$_ordersEndpoint/$orderId');
  }
}
