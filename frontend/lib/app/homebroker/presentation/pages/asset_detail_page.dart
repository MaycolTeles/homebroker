import 'package:flutter/material.dart';
import 'package:frontend/app/homebroker/api/entities/asset.dart';
import 'package:frontend/app/homebroker/api/entities/asset_daily.dart'
    show AssetDaily;
import 'package:frontend/app/homebroker/api/websocket/asset.dart'
    show AssetWebsocketAPI;
import 'package:frontend/app/homebroker/presentation/dialogs/dialogs.dart';
import 'package:frontend/app/homebroker/providers/asset_provider.dart'
    show AssetProvider;
import 'package:frontend/app/homebroker/services/asset_daily_service.dart'
    show AssetDailyService;
import 'package:frontend/app/homebroker/services/asset_service.dart';
import 'package:frontend/core/components/generic_error_dialog.dart';
import 'package:frontend/core/components/api/api_future_builder.dart';
import 'package:frontend/core/components/loading_overlay.dart';
import 'package:frontend/core/functions/platform.dart';
import 'package:gap/gap.dart' show Gap;
import 'package:intl/intl.dart';
import 'package:provider/provider.dart';
import 'package:syncfusion_flutter_charts/charts.dart';

class AssetDetailPage extends StatefulWidget {
  static const url = '/ativos/:id';
  final String assetId;

  const AssetDetailPage({
    super.key,
    required this.assetId,
  });

  @override
  State<AssetDetailPage> createState() => _AssetDetailPageState();
}

class _AssetDetailPageState extends State<AssetDetailPage> {
  final GlobalKey<LoadingOverlayState> _loadingOverlayKey =
      GlobalKey<LoadingOverlayState>();
  final TextEditingController sharesController =
      TextEditingController(text: "1");
  final TextEditingController priceController =
      TextEditingController(text: "0.00");
  late final AssetWebsocketAPI _websocket;
  List<AssetDaily> _assetsDailies = [];
  ChartSeriesController? _chartSeriesController;

  @override
  void initState() {
    super.initState();
    _setupWebsocket();
  }

  @override
  Widget build(BuildContext context) {
    Widget body = Padding(
      padding: const EdgeInsets.all(16.0),
      child: _getBody(),
    );

    return LoadingOverlay(
      key: _loadingOverlayKey,
      scaffold: getScaffoldAccordingToPlatform(body: body),
    );
  }

  @override
  void dispose() {
    _websocket.disconnect();
    super.dispose();
  }

  void _setupWebsocket() {
    _websocket = AssetWebsocketAPI(
      assetId: widget.assetId,
      onMessage: (data) => _receiveAssetDailyFromWebsocket(data),
    );
    _websocket.connect();
  }

  Padding _getBody() {
    Future<Asset> asset = AssetService.getAssetById(widget.assetId);
    Future<List<AssetDaily>> assetsDailies =
        AssetDailyService.getAllAssetsDailiesByAssetId(widget.assetId);

    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        children: [
          APIFutureBuilder<Asset>(
            future: asset,
            errorMessage: "Erro ao carregar ativo.",
            emptyDataMessage: "Ativo indisponível no momento.",
            builder: (asset) {
              _updateAssetProvider(asset);
              return _getAssetHeader(asset);
            },
          ),
          const Gap(32.0),
          _getQuantityAndPriceFields(),
          const Gap(16.0),
          _getBuyOrSellButtons(),
          const Gap(32.0),
          APIFutureBuilder<List<AssetDaily>>(
            future: assetsDailies,
            errorMessage: "Erro ao carregar histórico do ativo.",
            emptyDataMessage: "Histórico do ativo indisponível no momento.",
            builder: (assetsDailies) {
              _assetsDailies = assetsDailies;
              return Expanded(child: _getChart());
            },
          ),
        ],
      ),
    );
  }

  void _receiveAssetDailyFromWebsocket(Map<String, dynamic> data) {
    AssetDaily assetDaily = AssetDaily.fromJson(data);
    _assetsDailies.add(assetDaily);
    _chartSeriesController?.updateDataSource(
      addedDataIndexes: <int>[_assetsDailies.length - 1],
    );
  }

  Row _getAssetHeader(Asset asset) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Image.network(asset.imageUrl, height: 50),
        const Gap(16.0),
        Text(
          asset.name,
          style: const TextStyle(
            fontSize: 24,
            fontWeight: FontWeight.bold,
          ),
        ),
      ],
    );
  }

  Row _getQuantityAndPriceFields() {
    return Row(
      children: [
        Expanded(
          flex: 3,
          child: TextField(
            controller: sharesController,
            decoration: const InputDecoration(
              labelText: "Quantidade",
              border: OutlineInputBorder(),
            ),
            keyboardType: TextInputType.numberWithOptions(signed: true),
          ),
        ),
        Spacer(),
        Expanded(
          flex: 3,
          child: TextField(
            controller: priceController,
            decoration: const InputDecoration(
              labelText: "Preço",
              border: OutlineInputBorder(),
            ),
            keyboardType: TextInputType.numberWithOptions(
              decimal: true,
              signed: true,
            ),
          ),
        ),
      ],
    );
  }

  Row _getBuyOrSellButtons() {
    return Row(
      children: [
        Expanded(
          child: ElevatedButton(
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.green,
              padding: const EdgeInsets.all(16),
            ),
            onPressed: () => _handleBuyButton(),
            child: const Text("COMPRAR", style: TextStyle(fontSize: 18)),
          ),
        ),
        const Gap(16.0),
        Expanded(
          child: ElevatedButton(
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.red,
              padding: const EdgeInsets.all(16),
            ),
            onPressed: () => _handleSellButton(),
            child: const Text("VENDER", style: TextStyle(fontSize: 18)),
          ),
        ),
      ],
    );
  }

  void _updateAssetProvider(Asset asset) {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      Provider.of<AssetProvider>(context, listen: false).updateAsset(asset);
    });
  }

  SfCartesianChart _getChart() {
    return SfCartesianChart(
      trackballBehavior: TrackballBehavior(
        enable: true,
        activationMode: ActivationMode.longPress,
        tooltipSettings: const InteractiveTooltip(
          enable: true,
          format: 'point.x : point.y',
        ),
      ),
      primaryXAxis: DateTimeAxis(
        intervalType: DateTimeIntervalType.minutes,
        dateFormat: DateFormat.Hm(),
        majorGridLines: const MajorGridLines(width: 0),
        axisLine: const AxisLine(width: 0),
      ),
      primaryYAxis: NumericAxis(
        numberFormat: NumberFormat.simpleCurrency(
          locale: 'pt_BR',
          decimalDigits: 0,
        ),
        majorGridLines: const MajorGridLines(width: 0),
        axisLine: const AxisLine(width: 0),
      ),
      series: <LineSeries>[
        LineSeries<AssetDaily, DateTime>(
          dataSource: _assetsDailies,
          xValueMapper: (AssetDaily ad, _) => ad.datetime,
          yValueMapper: (AssetDaily ad, _) => ad.price,
          color: Colors.blue,
          onRendererCreated: (ChartSeriesController controller) {
            _chartSeriesController = controller;
          },
        ),
      ],
      tooltipBehavior: TooltipBehavior(
        enable: true,
        header: "",
      ),
      zoomPanBehavior: ZoomPanBehavior(
        enablePanning: true,
        enablePinching: true,
        zoomMode: ZoomMode.x,
        enableMouseWheelZooming: true,
      ),
      crosshairBehavior: CrosshairBehavior(
        enable: true,
        activationMode: ActivationMode.singleTap,
        lineType: CrosshairLineType.both,
      ),
    );
  }

  void _handleBuyButton() {
    bool valuesAreValid = _areSharesAndPriceValuesValid();
    if (!valuesAreValid) return;

    int shares = int.parse(sharesController.text);
    double price = double.parse(priceController.text);

    showBuyAssetDialog(shares, price);
  }

  void _handleSellButton() {
    bool valuesAreValid = _areSharesAndPriceValuesValid();
    if (!valuesAreValid) return;

    int shares = int.parse(sharesController.text);
    double price = double.parse(priceController.text);

    showSellAssetDialog(shares, price);
  }

  bool _areSharesAndPriceValuesValid() {
    String title = "Valor inválido!";
    String message = "";
    int shares;
    double price;

    try {
      shares = int.parse(sharesController.text);
    } on FormatException {
      message = "O número de ações deve ser um número!";
      showGenericErrorDialog(title: title, message: message);
      return false;
    }

    try {
      price = double.parse(priceController.text);
    } on FormatException {
      message = "O valor da ordem deve ser um número!";
      showGenericErrorDialog(title: title, message: message);
      return false;
    }

    if (shares < 1) {
      message = "O número de ações deve ser pelo menos 1!";
      showGenericErrorDialog(title: title, message: message);
      return false;
    }

    if (price <= 0) {
      message = "O valor da ordem deve ser maior que 0!";
      showGenericErrorDialog(title: title, message: message);
      return false;
    }

    return true;
  }
}
