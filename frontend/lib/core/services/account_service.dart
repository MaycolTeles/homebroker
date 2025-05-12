import 'package:frontend/app/account/api/entities/account.dart' show Account;
import 'package:frontend/app/account/api/requests/account.dart' show AccountAPI;

class AccountService {
  static Future<Account> getAccountById(String accountId) {
    Future<Account> account = AccountAPI.getAccountById(accountId);
    return account;
  }
}
