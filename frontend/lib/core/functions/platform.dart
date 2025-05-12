import 'dart:io';

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:frontend/core/components/navbars/navbar.dart';

Scaffold getScaffoldAccordingToPlatform({
  required Widget body,
  FloatingActionButton? floatingActionButton,
  Drawer? drawer,
}) {
  bool isMobile = _isRunningOnMobile();

  if (isMobile) return _getMobileScaffold(body, floatingActionButton, drawer);

  return _getWebOrDesktopScaffold(body, floatingActionButton);
}

bool _isRunningOnMobile() {
  return true; // TODO: REMOVE WHEN TESTING FOR WEB
  if (kIsWeb) return false;
  return Platform.isIOS || Platform.isAndroid;
}

Scaffold _getMobileScaffold(
  Widget body,
  FloatingActionButton? floatingActionButton,
  Drawer? drawer,
) {
  AppBar? appBar = _getMobileAppBar();

  return Scaffold(
    appBar: appBar,
    body: body,
    drawer: drawer,
    floatingActionButton: floatingActionButton,
    bottomNavigationBar: _getMobileBottomNavigationBar(),
  );
}

HomeBrokerBottomNavBar _getMobileBottomNavigationBar() {
  return HomeBrokerBottomNavBar();
}

AppBar _getMobileAppBar() {
  return AppBar(backgroundColor: Colors.black);
}

Scaffold _getWebOrDesktopScaffold(
  Widget body,
  FloatingActionButton? floatingActionButton,
) {
  return Scaffold(
    appBar: _getMobileAppBar(),
    body: body,
    floatingActionButton: Padding(
      padding: const EdgeInsets.all(8.0),
      child: floatingActionButton,
    ),
  );
}
