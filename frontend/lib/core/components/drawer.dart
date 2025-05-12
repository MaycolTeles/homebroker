import 'package:flutter/material.dart';
import 'package:frontend/app/account/api/requests/auth.dart' show AuthAPI;
import 'package:frontend/config/navigation/page_navigator.dart'
    show NavigationPage, PageNavigator;
import 'package:gap/gap.dart' show Gap;

Drawer getDrawer() {
  return Drawer(
    child: Padding(
      padding: const EdgeInsets.symmetric(
        horizontal: 8.0,
        vertical: 32.0,
      ),
      child: Column(
        children: [
          const Divider(),
          const Gap(16.0),
          ListTile(
            leading: const Icon(Icons.account_box),
            title: const Text("Minha Conta"),
            onTap: () => PageNavigator.navigateTo(NavigationPage.account),
          ),
          const Gap(16.0),
          ListTile(
            leading: const Icon(Icons.settings),
            title: const Text("Configurações"),
            onTap: () {},
          ),
          const Gap(16.0),
          ListTile(
            leading: const Icon(Icons.info),
            title: const Text("Sobre"),
            onTap: () => PageNavigator.navigateTo(NavigationPage.about),
          ),
          const Gap(16.0),
          Spacer(),
          ListTile(
            leading: const Icon(Icons.logout),
            title: const Text("Sair"),
            onTap: () {
              AuthAPI.signOut();
              PageNavigator.goTo(NavigationPage.login);
            },
          ),
          const Divider(),
        ],
      ),
    ),
  );
}
