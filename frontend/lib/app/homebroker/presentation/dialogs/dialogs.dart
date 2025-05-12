import 'package:flutter/material.dart';
import 'package:frontend/app/homebroker/api/entities/asset.dart' show Asset;
import 'package:frontend/app/homebroker/api/entities/order.dart';
import 'package:frontend/app/homebroker/providers/asset_provider.dart'
    show AssetProvider;
import 'package:frontend/app/homebroker/providers/wallet_provider.dart'
    show WalletProvider;
import 'package:frontend/app/homebroker/services/order_service.dart'
    show OrderService;
import 'package:frontend/core/functions/utils.dart' show getGlobalContext;
import 'package:provider/provider.dart';

void showBuyAssetDialog(
  int shares,
  double price,
) {
  BuildContext context = getGlobalContext();

  String walletId =
      Provider.of<WalletProvider>(context, listen: false).wallet?.id ??
          showPickWalletModal();
  Asset asset = Provider.of<AssetProvider>(context, listen: false).asset!;

  showDialog(
    context: context,
    builder: (BuildContext context) {
      return AlertDialog(
        insetPadding: const EdgeInsets.symmetric(
          horizontal: 48.0,
          vertical: 96.0,
        ),
        title: const Text("Confirme a Compra"),
        content: Text(
          'Tem certeza que deseja comprar $shares ações de ${asset.name} a R\$$price',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text("Cancelar"),
          ),
          TextButton(
            onPressed: () {
              OrderService.createOrder(
                asset.id,
                walletId,
                shares,
                price,
                OrderType.BUY,
              );
              Navigator.of(context).pop();
            },
            child: const Text("Comprar"),
          ),
        ],
      );
    },
  );
}

void showSellAssetDialog(
  int shares,
  double price,
) {
  BuildContext context = getGlobalContext();
  String walletId =
      Provider.of<WalletProvider>(context, listen: false).wallet?.id ??
          showPickWalletModal();
  Asset asset = Provider.of<AssetProvider>(context, listen: false).asset!;

  showDialog(
    context: context,
    builder: (BuildContext context) {
      return AlertDialog(
        insetPadding: const EdgeInsets.symmetric(
          horizontal: 48.0,
          vertical: 96.0,
        ),
        title: const Text("Confirme a Venda"),
        content: Text(
          'Tem certeza que deseja vender $shares ações de ${asset.name} a R\$$price',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text("Cancelar"),
          ),
          TextButton(
            onPressed: () {
              OrderService.createOrder(
                asset.id,
                walletId,
                shares,
                price,
                OrderType.SELL,
              );
              Navigator.of(context).pop();
            },
            child: const Text("Vender"),
          ),
        ],
      );
    },
  );
}

String showPickWalletModal() {
  // TODO: IMPLEMENT TO CHOOSE A WALLET TO ADD THAT ASSET TO.
  return "539b6b00-bb02-40ab-b5cc-a97644a49c6b";
}
