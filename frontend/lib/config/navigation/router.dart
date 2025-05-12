import 'package:frontend/app/account/presentation/routes.dart';
import 'package:frontend/app/homebroker/presentation/routes.dart';
import 'package:frontend/core/presentation/pages/error_page.dart';
import 'package:frontend/core/presentation/routes.dart';
import 'package:go_router/go_router.dart';

final GoRouter goRouter = GoRouter(
  initialLocation: '/',
  errorBuilder: (context, state) => const ErrorPage(),
  routes: _getRoutes(),
);

List<GoRoute> _getRoutes() {
  return [
    ...CommonRoutes.routes,
    ...AuthRoutes.routes,
    ...HomebrokerRoutes.routes,
  ];
}
