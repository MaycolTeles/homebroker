import 'package:frontend/app/homebroker/api/entities/order.dart'
    show Order, OrderType;
import 'package:frontend/app/homebroker/api/requests/order.dart'
    show OrderAPI, OrderDTO;

class OrderService {
  static void createOrder(
    String assetId,
    String walletId,
    int shares,
    double sharePrice,
    OrderType type,
  ) {
    OrderDTO dto = OrderDTO(
      assetId: assetId,
      walletId: walletId,
      shares: shares,
      sharePrice: sharePrice,
      type: type,
    );

    OrderAPI.createOrder(dto);
  }

  static Future<List<Order>> getAllOrders() {
    Future<List<Order>> orders = OrderAPI.getAllOrders();
    return orders;
  }

  static Future<Order> getOrderById(String orderId) {
    Future<Order> order = OrderAPI.getOrderById(orderId);
    return order;
  }
}
