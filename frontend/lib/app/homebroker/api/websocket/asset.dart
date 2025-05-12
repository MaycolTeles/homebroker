import 'package:frontend/app/homebroker/api/entities/asset_daily.dart'
    show AssetDaily;
import 'package:frontend/config/api/websocket.dart' show WebsocketAPI;

class AssetWebsocketAPI extends WebsocketAPI {
  final String assetId;

  AssetWebsocketAPI({
    required this.assetId,
    required super.onMessage,
  }) : super(endpoint: 'assets/$assetId');

  Stream<AssetDaily> get assetDailyStream =>
      stream.map((event) => AssetDaily.fromJson(event));
}
