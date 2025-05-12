import 'package:flutter/material.dart';
import 'package:frontend/core/components/drawer.dart' show getDrawer;
import 'package:frontend/core/constants.dart';
import 'package:frontend/core/functions/logo.dart';
import 'package:frontend/core/functions/platform.dart';
import 'package:gap/gap.dart';

class HomePage extends StatefulWidget {
  static const url = '/home';
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  @override
  Widget build(BuildContext context) {
    Drawer drawer = getDrawer();
    Widget body = _getBody();

    return getScaffoldAccordingToPlatform(
      body: body,
      drawer: drawer,
    );
  }

  Widget _getBody() {
    return Padding(
      padding: const EdgeInsets.all(32.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Gap(32.0),
          _getHeadliners(),
          const Gap(32.0),
          Column(
            children: [
              _getCard(),
              const Gap(64.0),
              getLogo(),
            ],
          ),
        ],
      ),
    );
  }

  Column _getHeadliners() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Bem vindo ao $appName!',
          style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
        ),
        const Gap(16.0),
        Text(
          'Acompanhe seus ativos e rentabilidade\nde forma prática e eficiente.',
          style: TextStyle(fontSize: 16),
        ),
      ],
    );
  }

  Card _getCard() {
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: _getCardContent(),
      ),
    );
  }

  Column _getCardContent() {
    return Column(
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              'Total Investido',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
            Text(
              'R\$ 50.000,00',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                color: Colors.green,
              ),
            ),
          ],
        ),
        const Gap(16.0),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              'Rentabilidade',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            Text(
              '+12.5%',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                color: Colors.blueAccent,
              ),
            ),
          ],
        ),
      ],
    );
  }
}
