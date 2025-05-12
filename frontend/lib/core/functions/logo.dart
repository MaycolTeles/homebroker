import 'package:flutter/material.dart';

String getImagePath(str) {
  return str;
  // return (kIsWeb) ? 'assets/$str' : str;
}

Image getLogo({double? width}) {
  width = width ?? 200;
  return Image.asset(
    getImagePath("assets/images/logos/homebroker.png"),
    width: width,
  );
}

// Text getAppName(BuildContext context, {TextStyle? style}) {
//   return Text(
//     appName,
//     style: Theme.of(context).primaryTextTheme.headlineLarge,
//   );
// }
