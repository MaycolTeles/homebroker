import 'package:flutter/material.dart';
import 'package:frontend/core/components/buttons/rectangular_button.dart';
import 'package:frontend/core/constants.dart';
import 'package:frontend/core/functions/logo.dart';
import 'package:frontend/config/navigation/page_navigator.dart';
import 'package:gap/gap.dart';

class WelcomePage extends StatefulWidget {
  static const url = '/';
  const WelcomePage({super.key});

  @override
  State<WelcomePage> createState() => _WelcomePageState();
}

class _WelcomePageState extends State<WelcomePage> {
  final bool _isAwaitingSignIn = false;

  @override
  void initState() {
    super.initState();
    // _goToHomeIfUserAlreadyLoggedInOnce();
  }

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        Scaffold(
          body: Column(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              getLogo(),
              _getWelcomeText(),
              const Gap(32.0),
              _getLoginButtons(),
            ],
          ),
        ),
        if (_isAwaitingSignIn)
          ModalBarrier(
            color: Colors.black.withOpacity(0.5),
            dismissible: false,
          )
        else
          const SizedBox.shrink(),
        if (_isAwaitingSignIn)
          const Center(
            child: CircularProgressIndicator(),
          )
        else
          const SizedBox.shrink()
      ],
    );
  }

  Row _getLoginButtons() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceAround,
      children: [
        RectangularButton(
          text: "Cadastre-se",
          onPressed: () => PageNavigator.goTo(NavigationPage.register),
        ),
        RectangularButton(
          text: "Faça Login",
          onPressed: () => PageNavigator.goTo(NavigationPage.login),
        ),
      ],
    );
  }

  Padding _getWelcomeText() {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          const Text("Seja Bem Vindo ao"),
          const Gap(16.0),
          Text(
            appName,
            style: Theme.of(context).primaryTextTheme.displayLarge,
          ),
          const Gap(32.0),
          const Text("Aqui você encontra o melhor homebroker"),
          const Text("que você vai usar na sua vida!"),
          const Gap(24.0),
          const Text("Faça seu cadastro e aproveite!"),
        ],
      ),
    );
  }

  // void _goToHomeIfUserAlreadyLoggedInOnce() async {
  //   bool userLogged = await checkIfTokenIsStoredInLocalStorage();

  //   if (userLogged) PageNavigator.goTo(NavigationPage.home);
  // }
}
