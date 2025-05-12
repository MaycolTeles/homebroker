class Asset {
  final String id;
  final DateTime createdAt;
  final DateTime updatedAt;
  final String name;
  final String symbol;
  final double price;
  final String imageUrl;

  Asset({
    required this.id,
    required this.createdAt,
    required this.updatedAt,
    required this.name,
    required this.symbol,
    required this.price,
    required this.imageUrl,
  });

  /// Convert JSON to Asset object
  factory Asset.fromJson(Map<String, dynamic> json) {
    return Asset(
      id: json['id'],
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: DateTime.parse(json['updated_at']),
      name: json['name'],
      symbol: json['symbol'],
      price: double.parse(json['price']),
      imageUrl: json['image_url'],
    );
  }

  /// Convert Asset object to JSON
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
      'name': name,
      'symbol': symbol,
      'price': price,
      'imageUrl': imageUrl,
    };
  }
}
