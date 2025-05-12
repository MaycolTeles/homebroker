import 'package:frontend/app/account/api/entities/account.dart' show Account;
import 'package:frontend/config/api/api.dart' show API;

class AccountAPI {
  static const String _accountsEndpoint = 'accounts';

  static Future<Account> getAccountById(String accountId) async {
    final response = await API.get('$_accountsEndpoint/$accountId');
    Account user = Account.fromJson(response.data);

    return user;
  }
}
