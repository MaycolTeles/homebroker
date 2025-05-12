import 'package:frontend/app/account/user_manager.dart';
import 'package:frontend/config/api/api.dart';
import 'package:frontend/config/api/token_manager.dart' show TokenManager;

class RegisterUserDTO {
  final String username;
  final String firstName;
  final String lastName;
  final String email;
  final String password;
  final String birthdate;

  RegisterUserDTO({
    required this.username,
    required this.firstName,
    required this.lastName,
    required this.email,
    required this.password,
    required this.birthdate,
  });

  Map<String, String> toJson() {
    return {
      'username': username,
      'first_name': firstName,
      'last_name': lastName,
      'email': email,
      'password': password,
      'birthdate': birthdate,
    };
  }
}

class LoginUserDTO {
  final String username;
  final String password;

  LoginUserDTO({
    required this.username,
    required this.password,
  });

  Map<String, String> toJson() {
    return {
      'username': username,
      'password': password,
    };
  }
}

class AuthAPI {
  static const String _authURL = 'auth';

  static Future<bool> registerUser(RegisterUserDTO dto) async {
    final body = dto.toJson();
    final response = await API.post('$_authURL/register', body: body);

    String userId = response.data['user_id'];
    UserManager().saveUserId(userId);

    String token = response.data['token'];
    TokenManager().saveToken(token);

    return Future.value(true); // TODO: UPDATE RETURN
  }

  static Future<bool> loginUser(LoginUserDTO dto) async {
    final body = dto.toJson();
    final response = await API.post('$_authURL/login', body: body);

    String userId = response.data['user_id'];
    UserManager().saveUserId(userId);

    String token = response.data['token'];
    TokenManager().saveToken(token);

    return Future.value(true); // TODO: UPDATE RETURN
  }

  // static Future<bool> validateGoogleToken(String token) async {
  //   String url = '$apiAuthURL/google/';
  //   Map<String, String> body = {'token': token};
  //   Map<String, dynamic> response = await API.post(url, body: body);

  //   bool tokenValid = response['token_valid'] ?? false;

  //   return Future.value(tokenValid);
  // }

  static Future<bool> signOut() async {
    // TODO: CHECK IF SUCCESSFUL
    String logoutURL = '$_authURL/logout';
    await API.post(logoutURL);
    TokenManager().deleteToken();

    return Future.value(true);
  }

  // TODO: CLEAR THIS FILE
}
