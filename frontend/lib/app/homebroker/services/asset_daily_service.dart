import 'package:frontend/app/homebroker/api/entities/asset_daily.dart'
    show AssetDaily;
import 'package:frontend/app/homebroker/api/requests/asset_daily.dart'
    show AssetDailyAPI;

class AssetDailyService {
  static Future<List<AssetDaily>> getAllAssetsDailiesByAssetId(String assetId) {
    Future<List<AssetDaily>> assetsDailies =
        AssetDailyAPI.getAllAssetsDailiesFilteredByAssetIdAndOrderedByDatetime(
            assetId);
    return assetsDailies;
  }
}
