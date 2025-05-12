import 'package:dio/dio.dart';
import 'package:flutter/cupertino.dart';
import 'package:frontend/config/api/exceptions/api_exception.dart'
    show APIException;
import 'package:frontend/config/api/token_manager.dart' show TokenManager;
import 'package:frontend/config/navigation/page_navigator.dart'
    show NavigationPage, PageNavigator;
import 'package:frontend/core/components/generic_error_dialog.dart'
    show showGenericErrorDialog;
import 'package:frontend/core/functions/utils.dart' show getGlobalContext;
import 'package:go_router/go_router.dart';

class ErrorHandlerInterceptor extends Interceptor {
  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    if (err.response == null) {
      String errorMessage =
          "Sem conexão com o servidor no momento.\nPor favor, verifique se você tem acesso à internet.";
      showGenericErrorDialog(message: errorMessage);
      return;
    }

    Response response = err.response!;
    switch (response.statusCode) {
      // Bad Request
      case 400:
        _handleBadRequestError(response);
        break;

      // Unauthorized
      case 401:
        // Wrong credentials (when logging in) or
        // Missing token (expired, for example)
        _handleUnauthorizedError(response);
        break;

      // Not Found
      case 404:
        String errorMessage =
            "Serviço não encontrado.\nPor favor, verifique novamente.";
        showGenericErrorDialog(message: errorMessage);
        break;

      case 500: // Internal Server Error
        String errorMessage =
            "Parece que o servidor não está respondendo.\nPor favor, tente novamente mais tarde.";
        showGenericErrorDialog(message: errorMessage);
        break;

      default:
        _handleBadRequestError(response);
        break;
    }

    return handler.next(err);
  }

  void _handleBadRequestError(Response response) {
    APIException error = APIException.fromResponse(response.data);
    showGenericErrorDialog(message: error.message);
  }

  void _handleUnauthorizedError(Response response) {
    _clearToken();

    APIException error = APIException.fromResponse(response.data);
    showGenericErrorDialog(
      message: error.message,
      callback: _navigateToLoginPage,
    );
  }
}

void _clearToken() {
  TokenManager().deleteToken();
}

void _navigateToLoginPage() {
  BuildContext context = getGlobalContext();
  if (context.canPop()) context.pop();
  PageNavigator.goTo(NavigationPage.login);
}
