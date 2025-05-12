import 'dart:convert' show json;
import 'package:frontend/config/api/token_manager.dart' show TokenManager;
import 'package:frontend/config/contants.dart' show API_DOMAIN;
import 'package:web_socket_channel/status.dart' as status;
import 'package:web_socket_channel/web_socket_channel.dart'
    show WebSocketChannel;

class WebsocketAPI {
  final String endpoint;
  final void Function(Map<String, dynamic>) onMessage;

  late final WebSocketChannel _channel;

  Stream<dynamic> get stream => _channel.stream;

  WebsocketAPI({
    required this.endpoint,
    required this.onMessage,
  });

  Future<bool> connect() async {
    Map<String, String> queryParameters = _getQueryParameters();

    Uri uri = Uri(
      scheme: 'ws',
      host: "localhost",
      port: 8080,
      path: 'ws/$endpoint/',
      queryParameters: queryParameters,
    );

    try {
      _channel = WebSocketChannel.connect(uri);
    } catch (e) {
      // TODO: UPDATE
      print("ERROR CONNECTING TO WEBSOCKET");
      return false;
    }

    try {
      _channel.stream.listen(
        (message) {
          final Map<String, dynamic> data = json.decode(message);
          onMessage(data);
        },
        onError: (error) {
          // TODO: HANDLE
          print("WebSocket error: $error");
        },
        onDone: () {
          // TODO: HANDLE
          print("WebSocket closed");
        },
      );
    } catch (e) {
      print("ERRO AQUI!!!");
    }

    return true;
  }

  void send(Map<String, dynamic> data) {
    _channel.sink.add(json.encode(data));
  }

  void disconnect() {
    _channel.sink.close(status.normalClosure);
  }

  /// Return the query parameters to send through websocket query parameters
  Map<String, String> _getQueryParameters() {
    Map<String, String> parameters = {};
    final String? token = TokenManager().token;

    bool tokenIsNullOrEmpty = token == null || token.isEmpty;
    if (tokenIsNullOrEmpty) return parameters;

    parameters = {'Authorization': token};

    return parameters;
  }
}
