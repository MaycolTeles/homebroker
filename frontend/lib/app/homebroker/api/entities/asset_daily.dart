class AssetDaily {
  final DateTime datetime;
  final double price;

  AssetDaily({
    required this.datetime,
    required this.price,
  });

  /// Convert JSON to AssetDaily object
  factory AssetDaily.fromJson(Map<String, dynamic> json) {
    return AssetDaily(
      datetime: DateTime.parse(json['datetime']),
      price: double.parse(json['price']),
    );
  }

  /// Convert AssetDaily object to JSON
  Map<String, dynamic> toJson() {
    return {
      'datetime': datetime.toIso8601String(),
      'price': price,
    };
  }
}
