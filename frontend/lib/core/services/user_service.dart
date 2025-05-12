import 'package:frontend/app/account/api/entities/user.dart' show User;
import 'package:frontend/app/account/api/requests/user.dart' show UserAPI;

class UserService {
  static Future<User> getUserById(String userId) {
    Future<User> user = UserAPI.getUserById(userId);
    return user;
  }
}
