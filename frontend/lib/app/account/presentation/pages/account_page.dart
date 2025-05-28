import 'package:flutter/material.dart';
import 'package:frontend/app/account/api/entities/account.dart' show Account;
import 'package:frontend/app/account/api/entities/user.dart' show User;
import 'package:frontend/app/account/api/requests/user.dart';
import 'package:frontend/app/account/user_manager.dart';
import 'package:frontend/core/components/api/api_future_builder.dart';
import 'package:frontend/core/functions/platform.dart';
import 'package:frontend/core/functions/utils.dart' show getUserFullName;

class AccountPage extends StatefulWidget {
  static const url = '/minha-conta';
  const AccountPage({super.key});

  @override
  State<AccountPage> createState() => _AccountPageState();
}

class _AccountPageState extends State<AccountPage> {
  late Future<User> _user;

  @override
  void initState() {
    super.initState();

    String? userId = UserManager().userId;
    _user = UserAPI.getUserById(userId!);
  }

  @override
  Widget build(BuildContext context) {
    Widget body = _getBody();
    return getScaffoldAccordingToPlatform(body: body);
  }

  Widget _getBody() {
    return Center(
      child: APIFutureBuilder<User>(
        future: _user,
        builder: (user) => _getData(user),
      ),
    );
  }

  Widget _getData(User user) {
    String username = getUserFullName(user);

    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Text(username),
        Padding(
          padding: const EdgeInsets.all(16.0),
          child: Text("Dados da Conta Investimento:"),
        ),
        _getAccounts(user.accounts[0]),
      ],
    );
  }

  Widget _getAccounts(Account account) {
    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.all(16.0),
          child: Text("Banco: ${account.bank}"),
        ),
        Padding(
          padding: const EdgeInsets.all(16.0),
          child: Text("Agência: ${account.agency}"),
        ),
        Padding(
          padding: const EdgeInsets.all(16.0),
          child: Text("Conta: ${account.accountNumber}"),
        ),
      ],
    );
  }
}
