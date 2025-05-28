import 'package:frontend/app/account/api/entities/account.dart' show Account;

class User {
  final String id;
  final DateTime createdAt;
  final DateTime updatedAt;
  final String firstName;
  final String lastName;
  final List<Account> accounts;

  User({
    required this.id,
    required this.createdAt,
    required this.updatedAt,
    required this.firstName,
    required this.lastName,
    required this.accounts,
  });

  /// Convert JSON to User object
  factory User.fromJson(Map<String, dynamic> json) {
    List<Account> accounts = (json['accounts'] as List)
        .map((account) => Account.fromJson(account))
        .toList();

    return User(
      id: json['id'],
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: DateTime.parse(json['updated_at']),
      firstName: json['first_name'],
      lastName: json['last_name'],
      accounts: accounts,
    );
  }
}
