import 'package:frontend/app/account/presentation/pages/create_password_page.dart';
import 'package:frontend/app/account/presentation/pages/login_page.dart';
import 'package:frontend/app/account/presentation/pages/register_page.dart';
import 'package:go_router/go_router.dart';

class AuthRoutes {
  static final List<GoRoute> routes = [
    GoRoute(
      path: CreatePasswordPage.url,
      builder: (context, state) {
        if (state.extra == null) return CreatePasswordPage(userData: const {});

        Map<String, dynamic> userData = state.extra as Map<String, dynamic>;
        return CreatePasswordPage(userData: userData);
      },
    ),
    GoRoute(
      path: LoginPage.url,
      builder: (context, state) => const LoginPage(),
    ),
    GoRoute(
      path: RegisterPage.url,
      builder: (context, state) => const RegisterPage(),
    ),
  ];
}
