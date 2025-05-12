import 'package:frontend/app/account/api/entities/user.dart' show User;
import 'package:frontend/config/api/api.dart' show API;

class UserAPI {
  static const String _usersEndpoint = 'users';

  static Future<User> getUserById(String userId) async {
    final response = await API.get('$_usersEndpoint/$userId');
    User user = User.fromJson(response.data);

    return user;
  }
}
