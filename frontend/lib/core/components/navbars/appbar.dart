import 'package:flutter/material.dart';
import 'package:frontend/config/navigation/page_navigator.dart';

class HomeBrokerAppBar extends StatelessWidget implements PreferredSizeWidget {
  const HomeBrokerAppBar({super.key});

  @override
  Widget build(BuildContext context) {
    List<Tab> tabs = [
      Tab(icon: Icon(Icons.home), text: 'Home'),
      Tab(icon: Icon(Icons.wallet), text: 'Carteiras'),
      Tab(icon: Icon(Icons.assessment_outlined), text: 'Ativos'),
      Tab(icon: Icon(Icons.my_library_books), text: 'Ordens'),
    ];

    return DefaultTabController(
      length: tabs.length,
      child: AppBar(
        bottom: TabBar(
          onTap: (index) => _navigateToPage(index),
          tabs: tabs,
          labelColor: Colors.black, // TODO: fix this const color
        ),
      ),
    );
  }

  @override
  Size get preferredSize => const Size.fromHeight(kToolbarHeight + 48);

  void _navigateToPage(int index) {
    switch (index) {
      case 0:
        PageNavigator.goTo(NavigationPage.home);
        break;

      case 1:
        PageNavigator.goTo(NavigationPage.walletList);
        break;

      case 2:
        PageNavigator.goTo(NavigationPage.assetList);
        break;

      case 3:
        PageNavigator.goTo(NavigationPage.orderList);
        break;
    }
  }
}
