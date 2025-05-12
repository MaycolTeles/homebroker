import 'package:frontend/app/homebroker/api/entities/wallet_asset.dart';
import 'package:frontend/config/api/api.dart';
import 'package:frontend/config/api/paginated_response.dart';

class CreateWalletAssetDTO {
  final String walletId;
  final String assetId;
  final int shares;

  CreateWalletAssetDTO({
    required this.walletId,
    required this.assetId,
    required this.shares,
  });

  /// Convert Wallet object to JSON
  Map<String, String> toJson() {
    return {
      'walletId': walletId,
      'assetId': assetId,
      'shares': shares.toString(),
    };
  }
}

class WalletAssetAPI {
  static const String _walletAssetsEndpoint = 'wallet-assets';

  static Future<List<WalletAsset>> getAllWalletAssets() async {
    final response = await API.get(_walletAssetsEndpoint);
    final paginatedResponse = PaginatedResponse.fromJson(
      response.data,
      (json) => WalletAsset.fromJson(json),
    );

    return paginatedResponse.results;
  }

  static Future<WalletAsset> getWalletAssetById(String walletAssetId) async {
    final response = await API.get('$_walletAssetsEndpoint/$walletAssetId');
    WalletAsset walletAsset = WalletAsset.fromJson(response.data);

    return walletAsset;
  }

  static Future<WalletAsset> createWalletAsset(CreateWalletAssetDTO dto) async {
    final body = dto.toJson();
    final response = await API.post(_walletAssetsEndpoint, body: body);
    WalletAsset walletAsset = WalletAsset.fromJson(response.data);

    return walletAsset;
  }

  static Future<void> deleteWalletAsset(String walletAssetId) async {
    final response = await API.delete('$_walletAssetsEndpoint/$walletAssetId');
  }
}
