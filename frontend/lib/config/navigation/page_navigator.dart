import 'package:frontend/app/account/presentation/pages/account_page.dart';
import 'package:frontend/app/account/presentation/pages/create_password_page.dart'
    show CreatePasswordPage;
import 'package:frontend/app/account/presentation/pages/login_page.dart'
    show LoginPage;
import 'package:frontend/app/account/presentation/pages/register_page.dart'
    show RegisterPage;
import 'package:frontend/app/homebroker/presentation/pages/asset_detail_page.dart'
    show AssetDetailPage;
import 'package:frontend/app/homebroker/presentation/pages/asset_list_page.dart'
    show AssetListPage;
import 'package:frontend/app/homebroker/presentation/pages/order_detail_page.dart'
    show OrderDetailPage;
import 'package:frontend/app/homebroker/presentation/pages/order_list_page.dart'
    show OrderListPage;
import 'package:frontend/app/homebroker/presentation/pages/wallet_detail_page.dart'
    show WalletDetailPage;
import 'package:frontend/app/homebroker/presentation/pages/wallet_list_page.dart'
    show WalletListPage;
import 'package:frontend/core/presentation/pages/about_page.dart'
    show AboutPage;
import 'package:frontend/core/presentation/pages/home_page.dart' show HomePage;
import 'package:frontend/core/presentation/pages/security_page.dart'
    show SecurityPage;
import 'package:frontend/core/presentation/pages/welcome_page.dart'
    show WelcomePage;
import 'package:go_router/go_router.dart' show GoRouter;

enum NavigationPage {
  welcome,
  login,
  register,
  createPassword,
  home,
  account,
  security,
  about,
  assetList,
  assetDetail,
  orderList,
  orderDetail,
  walletList,
  walletDetail,
}

Map<NavigationPage, String> _pageUrls = {
  NavigationPage.welcome: WelcomePage.url,
  NavigationPage.login: LoginPage.url,
  NavigationPage.register: RegisterPage.url,
  NavigationPage.createPassword: CreatePasswordPage.url,
  NavigationPage.home: HomePage.url,
  NavigationPage.account: AccountPage.url,
  NavigationPage.security: SecurityPage.url,
  NavigationPage.about: AboutPage.url,
  NavigationPage.assetList: AssetListPage.url,
  NavigationPage.assetDetail: AssetDetailPage.url,
  NavigationPage.orderList: OrderListPage.url,
  NavigationPage.orderDetail: OrderDetailPage.url,
  NavigationPage.walletList: WalletListPage.url,
  NavigationPage.walletDetail: WalletDetailPage.url,
};

class PageNavigator {
  static late GoRouter router;

  static void initialize(GoRouter goRouter) {
    router = goRouter;
  }

  /// Go back to the previous page.
  /// Go to the home page if there is no previous page.
  static void goBack({Map<String, dynamic>? arguments}) {
    if (!router.canPop()) {
      router.go(HomePage.url);
      return;
    }

    router.pop(arguments);
  }

  /// Go to a page without pushing a new page onto the page stack.
  static void goTo(
    NavigationPage page, {
    Map<String, dynamic>? arguments,
  }) {
    String routeName = _getRouteName(page, arguments: arguments);
    router.go(routeName, extra: arguments);
  }

  /// Push a new page onto the page stack.
  static void navigateTo(
    NavigationPage page, {
    Map<String, dynamic>? arguments,
  }) {
    String routeName = _getRouteName(page, arguments: arguments);
    router.push(routeName, extra: arguments);
  }

  static String _getRouteName(
    NavigationPage page, {
    Map<String, dynamic>? arguments,
  }) {
    String route = _pageUrls[page]!;

    // If arguments received, handle that by
    // adding the id to the url, for example
    if (arguments != null) {
      arguments.forEach((key, value) {
        route = route.replaceAll(':$key', value.toString());
      });
    }

    return route;
  }
}
