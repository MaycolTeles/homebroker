import 'package:flutter/material.dart';
import 'package:frontend/app/homebroker/api/entities/wallet.dart';
import 'package:frontend/app/homebroker/services/wallet_service.dart';
import 'package:frontend/config/navigation/page_navigator.dart';
import 'package:frontend/core/components/api/api_future_builder.dart';
import 'package:frontend/core/components/loading_overlay.dart';
import 'package:frontend/core/functions/platform.dart';
import 'package:gap/gap.dart';

class WalletListPage extends StatefulWidget {
  static const url = '/carteiras';
  const WalletListPage({super.key});

  @override
  State<WalletListPage> createState() => _WalletListPageState();
}

class _WalletListPageState extends State<WalletListPage> {
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
      scaffold: getScaffoldAccordingToPlatform(
        body: body,
        floatingActionButton: _getFloatingActionButton(),
      ),
    );
  }

  FloatingActionButton _getFloatingActionButton() {
    return FloatingActionButton(
      onPressed: () => showCreateWalletModal(context, _rebuildPage),
      child: const Icon(Icons.add),
    );
  }

  void _rebuildPage() => setState(() {});

  ListView _getBody() {
    return ListView(
      children: [
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Gap(32.0),
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: const Text(
                'Minhas carteiras 🚀',
                style: TextStyle(fontSize: 24),
              ),
            ),
            const Gap(32.0),
            getWalletsCards(),
            const Gap(32.0),
          ],
        ),
      ],
    );
  }

  APIFutureBuilder<List<Wallet>> getWalletsCards() {
    Future<List<Wallet>> wallets = WalletService.getAllWallets();

    return APIFutureBuilder<List<Wallet>>(
      future: wallets,
      errorMessage: "Erro ao carregar carteiras.",
      emptyDataMessage: "Sem carteiras no momento.",
      builder: (wallets) => _buildWalletsCards(wallets),
    );
  }

  ListView _buildWalletsCards(List<Wallet> wallets) {
    List<GestureDetector> cards = [];

    for (Wallet wallet in wallets) {
      cards.add(getWalletCard(wallet));
    }

    return ListView(
      shrinkWrap: true,
      physics: const ClampingScrollPhysics(),
      children: cards,
    );
  }

  GestureDetector getWalletCard(Wallet wallet) {
    return GestureDetector(
      onTap: () => navigateToWalletDetails(wallet.id),
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
                  wallet.name,
                  style: TextStyle(color: Colors.black),
                ),
                Text(
                  '${wallet.performance} %',
                  style: TextStyle(color: Colors.black),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  navigateToWalletDetails(String walletId) {
    Map<String, String> args = {'id': walletId};
    PageNavigator.navigateTo(NavigationPage.walletDetail, arguments: args);
  }
}

void showCreateWalletModal(
  BuildContext context,
  Function rebuildWidget,
) {
  TextEditingController controller = TextEditingController();

  showDialog(
    context: context,
    builder: (BuildContext context) {
      return AlertDialog(
        insetPadding: const EdgeInsets.symmetric(
          horizontal: 48.0,
          vertical: 96.0,
        ),
        title: const Text("Criar Carteira"),
        content: TextField(
          controller: controller,
          decoration: const InputDecoration(
            labelText: 'Nome da Carteira',
            border: OutlineInputBorder(),
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text("Cancelar"),
          ),
          TextButton(
            onPressed: () {
              WalletService.createWallet(controller.text);
              Navigator.of(context).pop();
              rebuildWidget();
            },
            child: const Text("OK"),
          ),
        ],
      );
    },
  );
}
