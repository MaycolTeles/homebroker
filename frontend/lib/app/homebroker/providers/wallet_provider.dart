import 'package:flutter/material.dart';
import 'package:frontend/app/homebroker/api/entities/wallet.dart';

class WalletProvider with ChangeNotifier {
  Wallet? _wallet;

  Wallet? get wallet => _wallet;

  void selectWallet(Wallet wallet) {
    _wallet = wallet;
    notifyListeners();
  }

  void updateWallet(Wallet updatedWallet) {
    _wallet = updatedWallet;
    notifyListeners();
  }

  void clearWallet() {
    _wallet = null;
    notifyListeners();
  }
}
