import 'package:flutter/material.dart';
import 'package:frontend/core/functions/logo.dart';
import 'package:frontend/config/navigation/page_navigator.dart';
import 'package:gap/gap.dart';

class ErrorPage extends StatelessWidget {
  const ErrorPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          children: [
            const Gap(96.0),
            getLogo(),
            const Gap(160.0),
            const Text('Página não encontrada =/'),
            const Gap(64.0),
            ElevatedButton(
              onPressed: () => PageNavigator.goTo(NavigationPage.home),
              child: const Text('Voltar'),
            ),
          ],
        ),
      ),
    );
  }
}
