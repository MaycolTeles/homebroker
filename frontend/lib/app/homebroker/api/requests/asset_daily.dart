import 'package:frontend/app/homebroker/api/entities/asset_daily.dart'
    show AssetDaily;
import 'package:frontend/config/api/api.dart';
import 'package:frontend/config/api/paginated_response.dart'
    show PaginatedResponse;

class AssetDailyAPI {
  static const String _assetsDailiesEndpoint = 'assets-dailies';

  static Future<List<AssetDaily>>
      getAllAssetsDailiesFilteredByAssetIdAndOrderedByDatetime(
    String assetId,
  ) async {
    Map<String, String> params = {'asset': assetId, 'ordering': 'datetime'};

    final response = await API.get(
      _assetsDailiesEndpoint,
      queryParameters: params,
    );
    final paginatedResponse = PaginatedResponse.fromJson(
      response.data,
      (json) => AssetDaily.fromJson(json),
    );

    return paginatedResponse.results;
  }
}
