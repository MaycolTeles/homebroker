import 'package:frontend/app/account/presentation/pages/account_page.dart'
    show AccountPage;
import 'package:frontend/core/presentation/pages/about_page.dart'
    show AboutPage;
import 'package:frontend/core/presentation/pages/home_page.dart' show HomePage;
import 'package:frontend/core/presentation/pages/security_page.dart'
    show SecurityPage;
import 'package:frontend/core/presentation/pages/welcome_page.dart'
    show WelcomePage;
import 'package:go_router/go_router.dart' show GoRoute;

class CommonRoutes {
  static final List<GoRoute> routes = [
    GoRoute(
      path: WelcomePage.url,
      builder: (context, state) => const WelcomePage(),
    ),
    GoRoute(
      path: HomePage.url,
      builder: (context, state) => const HomePage(),
    ),
    GoRoute(
      path: AccountPage.url,
      builder: (context, state) => const AccountPage(),
    ),
    GoRoute(
      path: SecurityPage.url,
      builder: (context, state) => const SecurityPage(),
    ),
    GoRoute(
      path: AboutPage.url,
      builder: (context, state) => const AboutPage(),
    ),
  ];
}
