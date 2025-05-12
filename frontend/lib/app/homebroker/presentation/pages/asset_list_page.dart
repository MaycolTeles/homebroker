import 'package:flutter/material.dart';
import 'package:frontend/app/homebroker/api/entities/asset.dart';
import 'package:frontend/app/homebroker/services/asset_service.dart';
import 'package:frontend/config/navigation/page_navigator.dart';
import 'package:frontend/core/components/api/api_future_builder.dart';
import 'package:frontend/core/components/loading_overlay.dart';
import 'package:frontend/core/functions/platform.dart';
import 'package:gap/gap.dart' show Gap;

class AssetListPage extends StatefulWidget {
  static const url = '/ativos';

  const AssetListPage({super.key});

  @override
  State<AssetListPage> createState() => _AssetListPageState();
}

class _AssetListPageState extends State<AssetListPage> {
  final GlobalKey<LoadingOverlayState> _loadingOverlayKey =
      GlobalKey<LoadingOverlayState>();

  @override
  Widget build(BuildContext context) {
    Widget body = Padding(
      padding: const EdgeInsets.all(16.0),
      child: _getBody(),
    );

    return LoadingOverlay(
      key: _loadingOverlayKey,
      scaffold: getScaffoldAccordingToPlatform(body: body),
    );
  }

  ListView _getBody() {
    return ListView(
      children: [
        Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            const Gap(32.0),
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: const Text(
                'Ativos',
                style: TextStyle(fontSize: 24),
              ),
            ),
            const Gap(16.0),
            getAssetsCards(),
            const Gap(32.0),
          ],
        ),
      ],
    );
  }

  APIFutureBuilder<List<Asset>> getAssetsCards() {
    Future<List<Asset>> assets = AssetService.getAllAssets();

    return APIFutureBuilder<List<Asset>>(
      future: assets,
      errorMessage: "Erro ao carregar ativos.",
      emptyDataMessage: "Sem ativos no momento.",
      builder: (assets) => _buildAssetsCards(assets),
    );
  }

  ListView _buildAssetsCards(List<Asset> assets) {
    List<GestureDetector> cards = [];

    for (Asset asset in assets) {
      cards.add(getAssetCard(asset));
    }

    return ListView(
      shrinkWrap: true,
      physics: const ClampingScrollPhysics(),
      children: cards,
    );
  }

  GestureDetector getAssetCard(Asset asset) {
    return GestureDetector(
      onTap: () => _navigateToAssetDetails(asset.id),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Card(
          elevation: 10,
          clipBehavior: Clip.antiAlias,
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  asset.name,
                  style: TextStyle(color: Colors.black),
                ),
                Text(
                  'R\$ ${asset.price.toStringAsPrecision(2)}',
                  style: TextStyle(color: Colors.black),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

_navigateToAssetDetails(String assetId) {
  Map<String, String> args = {'id': assetId};
  PageNavigator.navigateTo(NavigationPage.assetDetail, arguments: args);
}
