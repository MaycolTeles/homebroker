import 'package:flutter/material.dart';
import 'package:frontend/core/components/cards/card_info_row.dart' show InfoRow;
import 'package:frontend/core/components/cards/card_info_section.dart'
    show CardInfoSection;
import 'package:frontend/core/functions/datetime.dart';
import 'package:frontend/app/homebroker/api/entities/order.dart';

class OrderCardDetail extends StatelessWidget {
  final Order order;

  const OrderCardDetail({super.key, required this.order});

  @override
  Widget build(BuildContext context) {
    return CardInfoSection(
      children: [
        InfoRow(
          label: "Ativo",
          value: order.asset.name,
          icon: Icons.business,
        ),
        InfoRow(
          label: "Preço por Ação",
          value: "\$${order.sharePrice.toStringAsFixed(2)}",
          icon: Icons.price_check,
        ),
        InfoRow(
          label: "Número de Ações",
          value: "${order.shares}",
          icon: Icons.stacked_line_chart,
        ),
        InfoRow(
          label: "Ações Executadas",
          value: "${order.partial}",
          icon: Icons.task_alt,
        ),
        InfoRow(
          label: "Ordem Criada Em",
          value: getFormattedDateTimeInBRT(order.createdAt),
          icon: Icons.calendar_today,
        ),
        InfoRow(
          label: "Ordem Atualizada Em",
          value: getFormattedDateTimeInBRT(order.updatedAt),
          icon: Icons.update,
        ),
        const Divider(),
        InfoRow(
          label: "Valor Total da Ordem",
          value: "\$${order.totalPrice.toStringAsFixed(2)}",
          icon: Icons.attach_money,
          isBold: true,
        ),
      ],
    );
  }
}
