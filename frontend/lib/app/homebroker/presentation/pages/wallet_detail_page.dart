import 'package:flutter/material.dart';
import 'package:frontend/app/homebroker/api/entities/wallet.dart';
import 'package:frontend/app/homebroker/components/badge.dart' show BadgeLabel;
import 'package:frontend/app/homebroker/components/cards/wallet_card_detail.dart'
    show WalletCardDetail;
import 'package:frontend/app/homebroker/providers/wallet_provider.dart';
import 'package:frontend/app/homebroker/services/wallet_service.dart';
import 'package:frontend/config/navigation/page_navigator.dart';
import 'package:frontend/core/components/api/api_future_builder.dart';
import 'package:frontend/core/components/loading_overlay.dart';
import 'package:frontend/core/functions/platform.dart';
import 'package:gap/gap.dart';
import 'package:provider/provider.dart';

class WalletDetailPage extends StatefulWidget {
  static const url = '/carteiras/:id';
  final String walletId;

  const WalletDetailPage({
    super.key,
    required this.walletId,
  });

  @override
  State<WalletDetailPage> createState() => _WalletDetailPageState();
}

class _WalletDetailPageState extends State<WalletDetailPage> {
  final GlobalKey<LoadingOverlayState> _loadingOverlayKey =
      GlobalKey<LoadingOverlayState>();

  @override
  Widget build(BuildContext context) {
    Widget body = _getBody();

    return LoadingOverlay(
      key: _loadingOverlayKey,
      scaffold: getScaffoldAccordingToPlatform(
        body: body,
        floatingActionButton: _getFloatingActionButton(),
      ),
    );
  }

  FloatingActionButton _getFloatingActionButton() {
    return FloatingActionButton(
      onPressed: () => PageNavigator.navigateTo(NavigationPage.assetList),
      child: const Icon(Icons.add),
    );
  }

  Widget _getBody() {
    Future<Wallet> wallet = WalletService.getWalletById(widget.walletId);

    return ListView(
      shrinkWrap: true,
      children: [
        APIFutureBuilder<Wallet>(
          future: wallet,
          errorMessage: "Erro ao carregar carteira.",
          emptyDataMessage: "Carteira inválida.",
          builder: (wallet) {
            _updateWalletProvider(wallet);
            return _getWalletDetail(wallet);
          },
        ),
      ],
    );
  }

  void _updateWalletProvider(Wallet wallet) {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      Provider.of<WalletProvider>(context, listen: false).updateWallet(wallet);
    });
  }

  Widget _getWalletDetail(Wallet wallet) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        const Gap(16),
        Padding(
          padding: const EdgeInsets.all(16),
          child: Text(
            wallet.name,
            style: const TextStyle(fontSize: 24),
          ),
        ),
        const Gap(16),
        BadgeLabel(
          text: "Performance: ${wallet.performance}%",
          backgroundColor: wallet.performance >= 0
              ? Colors.green.shade100
              : Colors.red.shade100,
          textColor: wallet.performance >= 0 ? Colors.green : Colors.red,
        ),
        const Gap(32),
        WalletCardDetail(wallet: wallet),
        const Gap(32),
        _getAssetsSection(wallet),
        const Gap(64),
      ],
    );
  }

  Widget _getAssetsSection(Wallet wallet) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Padding(
          padding: EdgeInsets.all(16.0),
          child: Text(
            "Ativos",
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
        ),
        const Gap(8.0),
        ...wallet.walletAssets.map((walletAsset) {
          final asset = walletAsset.asset;
          return ListTile(
            leading: Image.network(asset.imageUrl, width: 40.0),
            title: Text(asset.name),
            subtitle: Text("${walletAsset.shares} ações - \$${asset.price}"),
            trailing: const Icon(Icons.arrow_forward_ios, size: 16.0),
            onTap: () => _navigateToAssetDetails(asset.id),
          );
        }),
      ],
    );
  }
}

_navigateToAssetDetails(String assetId) {
  Map<String, String> args = {'id': assetId};
  PageNavigator.navigateTo(NavigationPage.assetDetail, arguments: args);
}

void showDeleteWalletModal({
  required BuildContext context,
  required String walletId,
}) {
  showDialog(
    context: context,
    builder: (BuildContext context) {
      return AlertDialog(
        insetPadding: const EdgeInsets.symmetric(
          horizontal: 48.0,
          vertical: 96.0,
        ),
        title: const Text("Deletar Carteira"),
        content: Text('Tem certeza que deseja remover essa carteira?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text("Cancelar"),
          ),
          TextButton(
            onPressed: () => _handleWalletDelete(context, walletId),
            child: const Text("Remover carteira"),
          ),
        ],
      );
    },
  );
}

void _handleWalletDelete(BuildContext context, String walletId) async {
  Navigator.of(context).pop();
  bool walletDeleted = await WalletService.deleteWallet(walletId);

  if (walletDeleted) {
    PageNavigator.goBack();
  }
}
