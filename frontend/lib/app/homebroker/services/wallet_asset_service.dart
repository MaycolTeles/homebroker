import 'package:frontend/app/homebroker/api/requests/wallet_asset.dart';

class WalletAssetService {
  static void createWalletAsset(
    String walletId,
    String assetId,
    int shares,
    double price,
  ) {
    CreateWalletAssetDTO dto = CreateWalletAssetDTO(
      walletId: walletId,
      assetId:
          "33a0abe8-dad1-46ce-92a1-5c4126602522", // TODO: UPDATE THIS TO GET ASSET ID FROM THE APP
      shares: shares,
    );

    WalletAssetAPI.createWalletAsset(dto);
  }
}
