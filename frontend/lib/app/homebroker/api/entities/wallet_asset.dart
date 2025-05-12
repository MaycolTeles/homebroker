import 'package:frontend/app/homebroker/api/entities/asset.dart' show Asset;

class WalletAsset {
  final String id;
  final DateTime createdAt;
  final DateTime updatedAt;
  final Asset asset;
  final int shares;

  WalletAsset({
    required this.id,
    required this.createdAt,
    required this.updatedAt,
    required this.asset,
    required this.shares,
  });

  /// Convert JSON to Asset object
  factory WalletAsset.fromJson(Map<String, dynamic> json) {
    Asset asset = Asset.fromJson(json['asset']);

    return WalletAsset(
      id: json['id'],
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: DateTime.parse(json['updated_at']),
      shares: json['shares'],
      asset: asset,
    );
  }

  /// Convert Asset object to JSON
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
      'asset': asset.toJson(),
      'shares': shares,
    };
  }
}
