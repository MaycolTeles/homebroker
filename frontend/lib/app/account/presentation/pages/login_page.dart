import 'package:flutter/material.dart';
import 'package:frontend/app/account/api/requests/auth.dart';
import 'package:frontend/app/account/components/buttons/social_login_button.dart';
import 'package:frontend/app/account/components/form_fields/email_form_field.dart';
import 'package:frontend/app/account/components/form_fields/password_form_field.dart';
import 'package:frontend/core/components/buttons/rectangular_button.dart';
import 'package:frontend/core/functions/logo.dart';
import 'package:frontend/config/navigation/page_navigator.dart';
import 'package:gap/gap.dart';

class LoginPage extends StatefulWidget {
  static const url = '/login';

  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  final _formKey = GlobalKey<FormState>();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _getBody(context),
    );
  }

  Column _getBody(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        const Gap(16),
        getLogo(),
        const Gap(32),
        const Text("Bem vindo de volta. Sentimos a sua falta!"),
        const Gap(32),
        _getLoginForm(context),
        const Gap(32),
        _getLoginButton(),
        const Gap(32),
        _getDivider(),
        const Gap(32),
        _getSocialLoginButtons(),
        const Gap(32),
        _getRegisterButton(),
      ],
    );
  }

  Padding _getDivider() {
    return const Padding(
      padding: EdgeInsets.all(8.0),
      child: Row(
        children: [
          Expanded(
            child: Divider(
              thickness: 0.5,
              color: Colors.black,
            ),
          ),
          Padding(
            padding: EdgeInsets.all(8.0),
            child: Text(' Ou entre com '),
          ),
          Expanded(
            child: Divider(
              thickness: 0.5,
              color: Colors.black,
            ),
          ),
        ],
      ),
    );
  }

  Form _getLoginForm(BuildContext context) {
    return Form(
      key: _formKey,
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 54.0),
        child: Column(
          children: [
            EmailFormField(controller: _emailController),
            const Gap(15),
            PasswordFormField(controller: _passwordController),
            const Gap(10),
            Container(
              alignment: Alignment.centerRight,
              child: InkWell(
                onTap: () => _handleForgotPassword(),
                child: Text(
                  "Esqueceu a senha?",
                  style: TextStyle(
                    fontWeight: FontWeight.bold,
                    color: Theme.of(context).colorScheme.secondary,
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  RectangularButton _getLoginButton() {
    return RectangularButton(
      text: "Login",
      minimumSize: const Size(280, 60),
      onPressed: () {
        if (_formKey.currentState!.validate()) {
          _handleLoginUser();
        }
      },
    );
  }

  Row _getSocialLoginButtons() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        SocialLoginButton(image: "apple", onPressed: _handleAppleSignIn),
        const Gap(20),
        SocialLoginButton(image: "google", onPressed: _handleGoogleSignIn),
      ],
    );
  }

  Row _getRegisterButton() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        const Text('Não tem uma conta?'),
        const Gap(5),
        InkWell(
          onTap: () => PageNavigator.goTo(NavigationPage.register),
          child: Text(
            'Registre-se!',
            style: TextStyle(
              fontWeight: FontWeight.bold,
              color: Theme.of(context).colorScheme.secondary,
            ),
          ),
        ),
      ],
    );
  }

  Future<void> _handleLoginUser() async {
    final String email = _emailController.text;
    final String password = _passwordController.text;
    bool userLoggedIn = await _loginUserInAPI(email, password);

    if (userLoggedIn) PageNavigator.goTo(NavigationPage.home);
  }

  Future<bool> _loginUserInAPI(String email, String password) async {
    LoginUserDTO dto = LoginUserDTO(username: email, password: password);
    bool userLoggedIn = await AuthAPI.loginUser(dto);
    return userLoggedIn;
  }

  void _handleGoogleSignIn() async {
    // try {
    //   await GoogleAPI.handleSignIn();
    // } on UserNotRegisteredException catch (e) {
    //   showGenericErrorDialog(message: e.message);
    //   return;
    // }

    // PageNavigator.goTo(NavigationPage.home);
  }

  void _handleAppleSignIn() async {
    // TODO: Implement Apple Sign In logic here
  }

  void _handleForgotPassword() {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          insetPadding: const EdgeInsets.symmetric(
            horizontal: 48.0,
            vertical: 96.0,
          ),
          title: const Text("Recuperar senha"),
          content: TextField(
            // TODO: Implement email validation
            onChanged: (String value) => print(value),
            decoration: const InputDecoration(
              labelText: 'Email',
              border: OutlineInputBorder(),
            ),
            // content: Column(
            //   children: [
            //     const Text("Insira seu e-mail para recuperar sua senha."),
            //     const SizedBox(height: 30),
            //     TextFormField(
            //       decoration: const InputDecoration(
            //         labelText: 'Email',
            //         border: OutlineInputBorder(),
            //       ),
            //     ),
            //   ],
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: const Text("Cancelar"),
            ),
            TextButton(
              onPressed: () => _sendPasswordRecoveryEmail(),
              child: const Text("OK"),
            ),
          ],
        );
      },
    );
  }

  void _sendPasswordRecoveryEmail() {
    // TODO: Implement password recovery logic
    print("Sending password recovery email");
  }
}
