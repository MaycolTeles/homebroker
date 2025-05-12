import 'package:frontend/app/homebroker/api/entities/asset.dart' show Asset;

class Order {
  final String id;
  final DateTime createdAt;
  final DateTime updatedAt;
  final Asset asset;
  final int shares;
  final int partial;
  final double sharePrice;
  final double totalPrice;
  final OrderStatus status;
  final OrderType type;

  Order({
    required this.id,
    required this.createdAt,
    required this.updatedAt,
    required this.asset,
    required this.shares,
    required this.partial,
    required this.sharePrice,
    required this.totalPrice,
    required this.status,
    required this.type,
  });

  /// Convert JSON to Asset object
  factory Order.fromJson(Map<String, dynamic> json) {
    return Order(
      id: json['id'],
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: DateTime.parse(json['updated_at']),
      asset: Asset.fromJson(json['asset']),
      shares: json['shares'],
      partial: json['partial'],
      sharePrice: double.parse(json['share_price']),
      totalPrice: double.parse(json['total_price']),
      status: OrderStatus.values.byName(json['status']),
      type: OrderType.values.byName(json['type']),
    );
  }

  /// Convert Asset object to JSON
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
      'asset': asset.id,
      'shares': shares,
      'partial': partial,
      'share_price': sharePrice,
      'total_price': totalPrice,
      'status': status.name,
      'type': type.name,
    };
  }
}

enum OrderStatus {
  CLOSED,
  FAILED,
  OPEN,
  PENDING,
}

enum OrderType {
  BUY,
  SELL,
}
