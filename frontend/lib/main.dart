import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:frontend/app/account/user_manager.dart';
import 'package:frontend/app/homebroker/providers/asset_provider.dart'
    show AssetProvider;
import 'package:frontend/app/homebroker/providers/wallet_provider.dart';
import 'package:frontend/config/api/api.dart';
import 'package:frontend/config/api/interceptors/error_handler_interceptor.dart';
import 'package:frontend/config/api/token_manager.dart' show TokenManager;
import 'package:frontend/config/themes/themes.dart';
import 'package:frontend/config/navigation/page_navigator.dart';
import 'package:frontend/config/navigation/router.dart';
import 'package:frontend/core/constants.dart';
import 'package:go_router/go_router.dart';
import 'package:flutter_web_plugins/url_strategy.dart';
import 'package:intl/date_symbol_data_local.dart';
import 'package:intl/intl.dart';
import 'package:provider/provider.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await TokenManager().loadToken(); // Load token into memory
  await UserManager().loadUserId(); // Load userId into memory
  Intl.defaultLocale = 'pt_BR';
  initializeDateFormatting();
  usePathUrlStrategy();
  GoRouter.optionURLReflectsImperativeAPIs = true;
  dio.interceptors.addAll([
    // LogInterceptor(requestBody: true, responseBody: true),
    ErrorHandlerInterceptor(),
  ]);
  PageNavigator.initialize(goRouter);

  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => WalletProvider()),
        ChangeNotifierProvider(create: (_) => AssetProvider()),
      ],
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      routerConfig: goRouter,
      debugShowCheckedModeBanner: false,
      title: appName,
      theme: StyleThemes.lightTheme,
      darkTheme: StyleThemes.darkTheme,
      themeMode: ThemeMode.dark,
      localizationsDelegates: const [
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate
      ],
      supportedLocales: const [
        Locale('pt', 'BR'),
        Locale('en', 'US'),
      ],
    );
  }
}
