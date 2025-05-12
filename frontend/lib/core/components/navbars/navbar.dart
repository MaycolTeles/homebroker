import 'package:flutter/material.dart';
import 'package:frontend/config/navigation/page_navigator.dart';

class HomeBrokerBottomNavBar extends StatefulWidget {
  const HomeBrokerBottomNavBar({super.key});

  @override
  State<HomeBrokerBottomNavBar> createState() => _HomeBrokerBottomNavBarState();
}

class _HomeBrokerBottomNavBarState extends State<HomeBrokerBottomNavBar> {
  int _selectedIndex = 0;

  @override
  Widget build(BuildContext context) {
    return BottomNavigationBar(
      currentIndex: _selectedIndex,
      onTap: (index) => _onItemTapped(index),
      elevation: 10,
      showSelectedLabels: true,
      showUnselectedLabels: true,
      type: BottomNavigationBarType.fixed,
      items: const [
        BottomNavigationBarItem(
          icon: Icon(Icons.home),
          label: 'Home',
        ),
        BottomNavigationBarItem(
          icon: Icon(Icons.wallet),
          label: 'Carteiras',
        ),
        BottomNavigationBarItem(
          icon: Icon(Icons.assessment_outlined),
          label: 'Ativos',
        ),
        BottomNavigationBarItem(
          icon: Icon(Icons.my_library_books),
          label: 'Ordens',
        ),
      ],
    );
  }

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
      _navigateToPage(index);
    });
  }

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
