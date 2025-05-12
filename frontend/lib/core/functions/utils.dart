import 'package:flutter/material.dart';
import 'package:frontend/config/navigation/page_navigator.dart'
    show PageNavigator;

BuildContext getGlobalContext() =>
    PageNavigator.router.routerDelegate.navigatorKey.currentContext!;

String getShortenedId(String id) {
  return id.substring(0, 6);
}
