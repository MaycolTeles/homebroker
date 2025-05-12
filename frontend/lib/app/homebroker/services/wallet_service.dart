import 'package:frontend/app/homebroker/api/entities/wallet.dart';
import 'package:frontend/app/homebroker/api/requests/wallet.dart';

class WalletService {
  static Future<List<Wallet>> getAllWallets() {
    Future<List<Wallet>> wallets = WalletAPI.getAllWallets();
    return wallets;
  }

  static Future<Wallet> getWalletById(String walletId) {
    Future<Wallet> wallet = WalletAPI.getWalletById(walletId);
    return wallet;
  }

  static void createWallet(String walletName) {
    CreateWalletDTO dto = CreateWalletDTO(
      name: walletName,
      userId:
          "33a0abe8-dad1-46ce-92a1-5c4126602522", // TODO: UPDATE THIS TO GET USER ID FROM THE APP
    );
    WalletAPI.createWallet(dto);
  }

  static Future<bool> deleteWallet(String walletId) {
    Future<bool> walletDeleted = WalletAPI.deleteWallet(walletId);
    return walletDeleted;
  }
}
