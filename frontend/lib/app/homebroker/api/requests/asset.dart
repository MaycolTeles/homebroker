import 'package:frontend/app/homebroker/api/entities/asset.dart';
import 'package:frontend/config/api/api.dart';
import 'package:frontend/config/api/paginated_response.dart';

class AssetAPI {
  static const String _assetsEndpoint = 'assets';

  static Future<List<Asset>> getAllAssets() async {
    final response = await API.get(_assetsEndpoint);

    final paginatedResponse = PaginatedResponse.fromJson(
      response.data,
      (json) => Asset.fromJson(json),
    );

    return paginatedResponse.results;
  }

  static Future<Asset> getAssetById(String assetId) async {
    final response = await API.get('$_assetsEndpoint/$assetId');
    Asset asset = Asset.fromJson(response.data);

    return asset;
  }
}
