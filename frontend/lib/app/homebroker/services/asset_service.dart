import 'package:frontend/app/homebroker/api/entities/asset.dart';
import 'package:frontend/app/homebroker/api/requests/asset.dart';

class AssetService {
  static Future<List<Asset>> getAllAssets() {
    Future<List<Asset>> assets = AssetAPI.getAllAssets();
    return assets;
  }

  static Future<Asset> getAssetById(String assetId) {
    Future<Asset> asset = AssetAPI.getAssetById(assetId);
    return asset;
  }
}
