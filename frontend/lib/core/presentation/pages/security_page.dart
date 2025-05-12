import 'package:flutter/material.dart';
import 'package:frontend/config/navigation/page_navigator.dart';
import 'package:gap/gap.dart';

class SecurityPage extends StatefulWidget {
  static const url = '/seguranca';
  const SecurityPage({super.key});

  @override
  State<SecurityPage> createState() => _SecurityPageState();
}

class _SecurityPageState extends State<SecurityPage> {
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

  Column _getBody() {
    const String securityText =
        "Este aplicativo não tem intenção de coletar dados sensíveis. Seus dados são armazenados de forma segura e não são compartilhados com terceiros.";

    return const Column(
      children: [
        Gap(256.0),
        Text(
          "SOBRE SUA SEGURANÇA",
          style: TextStyle(fontWeight: FontWeight.bold),
        ),
        Padding(
          padding: EdgeInsets.all(48.0),
          child: Text(
            securityText,
            textAlign: TextAlign.center,
          ),
        ),
      ],
    );
  }
}
