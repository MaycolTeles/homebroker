import 'package:flutter/material.dart';
import 'package:frontend/app/homebroker/api/entities/asset.dart';

class AssetProvider with ChangeNotifier {
  Asset? _asset;

  Asset? get asset => _asset;

  void updateAsset(Asset updatedAsset) {
    _asset = updatedAsset;
    notifyListeners();
  }
}
