import 'package:flutter/material.dart' show debugPrint;
import 'package:frontend/config/api/exceptions/error_code_to_message_map.dart'
    show errorCodeMessageMap;

class APIException implements Exception {
  final String code;
  final String message;

  APIException(this.code, this.message);

  factory APIException.fromResponse(Map<String, dynamic> data) {
    final code = data["code"] ?? "unknown_error";
    final message = errorCodeMessageMap[code] ??
        data["detail"] ??
        "Erro desconhecido.\nPor favor, tente novamente mais tarde.";

    if (code != null && !errorCodeMessageMap.containsKey(code)) {
      debugPrint("⚠️ Unmapped API error code: $code");
    }

    return APIException(code, message);
  }
}
