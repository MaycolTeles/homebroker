import 'package:dio/dio.dart';
import 'package:frontend/config/api/token_manager.dart' show TokenManager;
import 'package:frontend/config/contants.dart' show API_DOMAIN;

final dio = Dio(
  BaseOptions(connectTimeout: const Duration(seconds: 3)),
);

const String API_BASE_URL = "http://$API_DOMAIN/api";

class API {
  static Future<Response> get(
    String url, {
    Map<String, dynamic>? queryParameters,
  }) async {
    Options options = Options(headers: _getHeaders());
    Response response = await dio.get(
      '$API_BASE_URL/$url/',
      queryParameters: queryParameters,
      options: options,
    );

    return response;
  }

  static Future<Response> post(
    String url, {
    Map<String, dynamic>? body,
  }) async {
    Options options = Options(headers: _getHeaders());
    Response response = await dio.post(
      '$API_BASE_URL/$url/',
      data: body,
      options: options,
    );

    return response;
  }

  static Future<Response> put(
    String url, {
    Map<String, dynamic>? body,
  }) async {
    Options options = Options(headers: _getHeaders());
    Response response = await dio.put(
      '$API_BASE_URL/$url/',
      data: body,
      options: options,
    );

    return response;
  }

  static Future<Response> patch(
    String url, {
    Map<String, dynamic>? body,
  }) async {
    Options options = Options(headers: _getHeaders());
    Response response = await dio.patch(
      '$API_BASE_URL/$url/',
      data: body,
      options: options,
    );

    return response;
  }

  static Future<Response> delete(
    String url, {
    Map<String, dynamic>? body,
  }) async {
    Options options = Options(headers: _getHeaders());
    Response response = await dio.delete(
      '$API_BASE_URL/$url/',
      data: body,
      options: options,
    );

    return response;
  }

  /// Return the headers to make the API call
  static Map<String, String> _getHeaders() {
    Map<String, String> headers = {};
    final String? token = TokenManager().token;

    bool tokenIsNullOrEmpty = token == null || token.isEmpty;
    if (tokenIsNullOrEmpty) return headers;

    headers = {'Authorization': 'Bearer $token'};

    return headers;
  }
}
