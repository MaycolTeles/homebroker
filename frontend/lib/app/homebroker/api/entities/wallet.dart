import 'package:frontend/app/homebroker/api/entities/wallet_asset.dart';

class Wallet {
  final String id;
  final DateTime createdAt;
  final DateTime updatedAt;
  final String name;
  final double totalInvested;
  final double currentBalance;
  final double performance;
  final List<WalletAsset> walletAssets;

  Wallet({
    required this.id,
    required this.createdAt,
    required this.updatedAt,
    required this.name,
    required this.totalInvested,
    required this.currentBalance,
    required this.performance,
    required this.walletAssets,
  });

  /// Convert JSON to Wallet object
  factory Wallet.fromJson(Map<String, dynamic> json) {
    List<WalletAsset> walletAssets = [];

    walletAssets = (json['assets'] as List?)
            ?.map((walletAsset) => WalletAsset.fromJson(walletAsset))
            .toList() ??
        []; // Convert into a List of Assets (or empty list)

    return Wallet(
      id: json['id'],
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: DateTime.parse(json['updated_at']),
      name: json['name'],
      totalInvested: double.parse(json['total_invested']),
      currentBalance: double.parse(json['current_balance']),
      performance: double.parse(json['performance']),
      walletAssets: walletAssets,
    );
  }

  /// Convert Wallet object to JSON
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
      'name': name,
      'total_invested': totalInvested,
      'current_balance': currentBalance,
      'performance': performance,
      'assets': walletAssets.map((asset) => asset.toJson()).toList(),
    };
  }
}
