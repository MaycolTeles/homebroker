import 'package:flutter/material.dart';
import 'package:frontend/config/navigation/page_navigator.dart';

void showGenericErrorDialog({
  String? title,
  String? message,
  Function()? callback,
}) {
  String errorTitle = title ?? "Erro";
  String errorMessage =
      message ?? "Um erro ocorreu.\nTente novamente mais tarde.";

  BuildContext? context =
      PageNavigator.router.routerDelegate.navigatorKey.currentContext;
  showDialog(
    barrierDismissible: false,
    context: context!,
    builder: (BuildContext context) {
      Function onPressed = callback ?? Navigator.of(context).pop;
      return PopScope(
        canPop: false,
        child: AlertDialog(
          insetPadding: const EdgeInsets.all(50),
          title: Text(errorTitle),
          content: Text(errorMessage),
          actions: [
            TextButton(
              onPressed: () => onPressed(),
              child: const Text("OK"),
            ),
          ],
        ),
      );
    },
  );
}
