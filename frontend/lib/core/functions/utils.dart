import 'package:flutter/material.dart';
import 'package:frontend/app/account/api/entities/user.dart' show User;
import 'package:frontend/config/navigation/page_navigator.dart'
    show PageNavigator;

BuildContext getGlobalContext() =>
    PageNavigator.router.routerDelegate.navigatorKey.currentContext!;

String getShortenedId(String id) {
  return id.substring(0, 6);
}

String getUserFullName(User user) {
  return '${user.firstName} ${user.lastName}';
}
