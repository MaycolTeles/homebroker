import 'package:frontend/app/homebroker/api/entities/wallet.dart';
import 'package:frontend/config/api/api.dart';
import 'package:frontend/config/api/paginated_response.dart';

class CreateWalletDTO {
  final String name;
  final String userId;

  CreateWalletDTO({
    required this.name,
    required this.userId,
  });

  /// Convert Wallet object to JSON
  Map<String, String> toJson() {
    return {
      'name': name,
      'user': userId,
    };
  }
}

class WalletAPI {
  static const String _walletsEndpoint = 'wallets';

  static Future<List<Wallet>> getAllWallets() async {
    final response = await API.get(_walletsEndpoint);
    final paginatedResponse = PaginatedResponse.fromJson(
      response.data,
      (json) => Wallet.fromJson(json),
    );

    return paginatedResponse.results;
  }

  static Future<Wallet> getWalletById(String walletId) async {
    final response = await API.get('$_walletsEndpoint/$walletId');
    Wallet wallet = Wallet.fromJson(response.data);

    return wallet;
  }

  static Future<Wallet> createWallet(CreateWalletDTO dto) async {
    final body = dto.toJson();
    final response = await API.post(_walletsEndpoint, body: body);
    Wallet wallet = Wallet.fromJson(response.data);

    return wallet;
  }

  static Future<bool> deleteWallet(String walletId) async {
    final response = await API.delete('$_walletsEndpoint/$walletId');

    if (response.statusCode! < 300) return true;
    return false;
  }
}
