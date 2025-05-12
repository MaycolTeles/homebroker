import 'package:flutter/material.dart';
import 'package:frontend/config/navigation/page_navigator.dart';
import 'package:gap/gap.dart';

class AboutPage extends StatefulWidget {
  static const url = '/sobre';
  const AboutPage({super.key});

  @override
  State<AboutPage> createState() => _AboutPageState();
}

class _AboutPageState extends State<AboutPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: _getAppBar(),
      body: _getBody(),
    );
  }

  AppBar _getAppBar() {
    return AppBar(
      leading: IconButton(
        icon: const Icon(Icons.arrow_back),
        onPressed: () => PageNavigator.goBack(),
      ),
    );
  }

  Padding _getBody() {
    const String aboutText =
        "Este homebroker foi desenvolvido para possibilitar a criação de ordens e análises de ativos listados na bolsa de valores.";

    const String disclaimerText =
        "Esse aplicativo não se responsabiliza por quaisquer possíveis perdas financeiras por parte do usuário. Invista com responsabilidade!";

    return const Padding(
      padding: EdgeInsets.symmetric(horizontal: 32.0),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Padding(
            padding: EdgeInsets.only(bottom: 32.0),
            child: Text(
              aboutText,
              textAlign: TextAlign.center,
            ),
          ),
          Text(
            disclaimerText,
            textAlign: TextAlign.center,
          ),
          Gap(128.0),
        ],
      ),
    );
  }
}
