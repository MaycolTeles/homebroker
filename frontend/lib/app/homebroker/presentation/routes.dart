import 'package:frontend/app/homebroker/presentation/pages/asset_detail_page.dart';
import 'package:frontend/app/homebroker/presentation/pages/asset_list_page.dart';
import 'package:frontend/app/homebroker/presentation/pages/order_detail_page.dart';
import 'package:frontend/app/homebroker/presentation/pages/order_list_page.dart';
import 'package:frontend/app/homebroker/presentation/pages/wallet_detail_page.dart';
import 'package:frontend/app/homebroker/presentation/pages/wallet_list_page.dart';
import 'package:go_router/go_router.dart';

class HomebrokerRoutes {
  static final List<GoRoute> routes = [
    GoRoute(
      path: AssetListPage.url,
      builder: (context, state) => const AssetListPage(),
    ),
    GoRoute(
      path: AssetDetailPage.url,
      builder: (context, state) {
        final assetId = state.pathParameters['id']!;
        return AssetDetailPage(assetId: assetId);
      },
    ),
    GoRoute(
      path: WalletListPage.url,
      builder: (context, state) => const WalletListPage(),
    ),
    GoRoute(
      path: WalletDetailPage.url,
      builder: (context, state) {
        final walletId = state.pathParameters['id']!;
        return WalletDetailPage(walletId: walletId);
      },
    ),
    GoRoute(
      path: OrderListPage.url,
      builder: (context, state) => const OrderListPage(),
    ),
    GoRoute(
      path: OrderDetailPage.url,
      builder: (context, state) {
        final orderId = state.pathParameters['id']!;
        return OrderDetailPage(orderId: orderId);
      },
    ),
  ];
}
