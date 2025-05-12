class Account {
  final String id;
  final DateTime createdAt;
  final DateTime updatedAt;
  final String bank;
  final String agency;
  final String accountNumber;

  Account({
    required this.id,
    required this.createdAt,
    required this.updatedAt,
    required this.bank,
    required this.agency,
    required this.accountNumber,
  });

  /// Convert JSON to Account object
  factory Account.fromJson(Map<String, dynamic> json) {
    return Account(
      id: json['id'],
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: DateTime.parse(json['updated_at']),
      bank: json['bank'],
      agency: json['agency'],
      accountNumber: json['account_number'],
    );
  }
}
