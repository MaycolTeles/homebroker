import 'package:flutter/material.dart';
import 'package:frontend/core/components/cards/card_info_row.dart' show InfoRow;
import 'package:frontend/core/components/cards/card_info_section.dart'
    show CardInfoSection;
import 'package:frontend/core/functions/datetime.dart'
    show getFormattedDateTimeInBRT;
import 'package:frontend/app/homebroker/api/entities/wallet.dart' show Wallet;

class WalletCardDetail extends StatelessWidget {
  final Wallet wallet;

  const WalletCardDetail({super.key, required this.wallet});

  @override
  Widget build(BuildContext context) {
    return CardInfoSection(
      children: [
        InfoRow(
          label: "Criado em",
          value: getFormattedDateTimeInBRT(wallet.createdAt),
          icon: Icons.calendar_today,
        ),
        InfoRow(
          label: "Atualizado em",
          value: getFormattedDateTimeInBRT(wallet.updatedAt),
          icon: Icons.update,
        ),
        InfoRow(
          label: "Total Investido",
          value: "\$${wallet.totalInvested}",
          icon: Icons.attach_money,
        ),
        InfoRow(
          label: "Saldo Atual",
          value: "\$${wallet.currentBalance}",
          icon: Icons.trending_up,
        ),
        InfoRow(
          label: "Performance",
          value: "${wallet.performance}%",
          icon: Icons.trending_up,
          isBold: true,
        ),
      ],
    );
  }
}
