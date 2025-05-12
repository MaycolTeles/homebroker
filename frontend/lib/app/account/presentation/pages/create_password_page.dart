import 'package:flutter/material.dart';
import 'package:frontend/app/account/api/requests/auth.dart'
    show AuthAPI, RegisterUserDTO;
import 'package:frontend/app/account/components/form_fields/password_confirmation_form_field.dart';
import 'package:frontend/app/account/components/form_fields/password_form_field.dart';
import 'package:frontend/core/components/loading_overlay.dart';
import 'package:frontend/core/functions/logo.dart';
import 'package:frontend/config/navigation/page_navigator.dart';
import 'package:gap/gap.dart';

class CreatePasswordPage extends StatelessWidget {
  static const url = '/criar-senha';

  final Map<String, dynamic> userData;

  CreatePasswordPage({
    super.key,
    required this.userData,
  });

  final GlobalKey<LoadingOverlayState> _loadingOverlayKey =
      GlobalKey<LoadingOverlayState>();

  final _formKey = GlobalKey<FormState>();

  final TextEditingController _passwordController = TextEditingController();

  final TextEditingController _passwordConfirmationController =
      TextEditingController();

  @override
  Widget build(BuildContext context) {
    if (userData.isEmpty) {
      PageNavigator.goTo(NavigationPage.register);
    }

    return LoadingOverlay(
      key: _loadingOverlayKey,
      scaffold: Scaffold(body: _getBody()),
    );
  }

  Column _getBody() {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        getLogo(),
        const Gap(64.0),
        const Text("Quase lá! Só falta criar uma senha!"),
        const Padding(
          padding: EdgeInsets.symmetric(horizontal: 16.0),
          child: Text("Use essa senha para poder acessar a sua conta depois.",
              softWrap: true, textAlign: TextAlign.center),
        ),
        const Gap(80.0),
        _getCreatePasswordForm(),
      ],
    );
  }

  Form _getCreatePasswordForm() {
    return Form(
      key: _formKey,
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 64.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            PasswordFormField(controller: _passwordController),
            const Gap(16.0),
            PasswordConfirmationFormField(
              passwordController: _passwordController,
              passwordConfirmationController: _passwordConfirmationController,
            ),
            const Gap(64.0),
            _getCreateAccountButton(),
          ],
        ),
      ),
    );
  }

  ElevatedButton _getCreateAccountButton() {
    return ElevatedButton(
      style: ElevatedButton.styleFrom(
        minimumSize: const Size(280, 60),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(10.0),
        ),
      ),
      onPressed: () {
        if (_formKey.currentState!.validate()) {
          _handleCreateAccount();
        }
      },
      child: const Text('Criar conta!'),
    );
  }

  void _handleCreateAccount() async {
    _pauseForRegister();

    userData['password'] = _passwordController.text;

    RegisterUserDTO dto = RegisterUserDTO(
      username: userData['username'],
      firstName: userData['firstName'],
      lastName: userData['lastName'],
      email: userData['email'],
      password: userData['password'],
      birthdate: userData['birthdate'],
    );

    try {
      await AuthAPI.registerUser(dto);
    } catch (e) {
      _resumeAfterRegister();
      return;
    }

    _resumeAfterRegister();
    PageNavigator.goTo(NavigationPage.home);
  }

  void _pauseForRegister() {
    _loadingOverlayKey.currentState!.pause();
  }

  void _resumeAfterRegister() {
    _loadingOverlayKey.currentState!.resume();
  }
}
