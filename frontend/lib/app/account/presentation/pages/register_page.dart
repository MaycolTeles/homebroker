import 'package:flutter/material.dart';
import 'package:frontend/app/account/components/buttons/social_login_button.dart';
import 'package:frontend/app/account/components/form_fields/custom_form_field.dart';
import 'package:frontend/app/account/components/form_fields/date_form_field.dart';
import 'package:frontend/app/account/components/form_fields/email_form_field.dart';
import 'package:frontend/core/components/buttons/rectangular_button.dart';
import 'package:frontend/core/components/loading_overlay.dart';
import 'package:frontend/core/functions/datetime.dart';
import 'package:frontend/core/functions/logo.dart';
import 'package:frontend/config/navigation/page_navigator.dart';
import 'package:gap/gap.dart';

class RegisterPage extends StatefulWidget {
  static const url = '/registrar';

  const RegisterPage({super.key});

  @override
  State<RegisterPage> createState() => _RegisterPageState();
}

class _RegisterPageState extends State<RegisterPage> {
  final GlobalKey<LoadingOverlayState> _loadingOverlayKey =
      GlobalKey<LoadingOverlayState>();

  final _formKey = GlobalKey<FormState>();

  final TextEditingController _nameController = TextEditingController();
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _dateController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return LoadingOverlay(
      key: _loadingOverlayKey,
      scaffold: Scaffold(body: _getBody()),
    );
  }

  ListView _getBody() {
    return ListView(
      children: [
        Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            const Gap(32.0),
            getLogo(),
            const Gap(32.0),
            const Text('Seja bem vindo!'),
            const Gap(8.0),
            const Padding(
              padding: EdgeInsets.all(16.0),
              child: Text(
                'Crie uma conta para conhecer o melhor homebroker\ndesenvolvido especialmente para você!',
                textAlign: TextAlign.center,
              ),
            ),
            const Gap(40.0),
            _getRegisterForm(),
            const Gap(16.0),
            _getRegisterButton(),
            const Gap(32.0),
            _getDivider(),
            const Gap(16.0),
            _getSocialRegisterButtons(),
            const Gap(32.0),
            _getLoginButton(),
            const Gap(32.0),
          ],
        ),
      ],
    );
  }

  Form _getRegisterForm() {
    return Form(
      key: _formKey,
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 54.0),
        child: Column(
          children: [
            CustomFormField(controller: _nameController, labelText: "Nome"),
            const Gap(15),
            EmailFormField(controller: _emailController),
            const Gap(15),
            DateFormField(controller: _dateController),
            const Gap(15)
          ],
        ),
      ),
    );
  }

  RectangularButton _getRegisterButton() {
    return RectangularButton(
      text: "Registrar",
      minimumSize: const Size(280, 60),
      onPressed: () {
        if (_formKey.currentState!.validate()) {
          _handleRegister();
        }
      },
    );
  }

  Padding _getDivider() {
    return const Padding(
      padding: EdgeInsets.all(8.0),
      child: Row(
        children: [
          Expanded(
            child: Divider(thickness: 0.5),
          ),
          Padding(
            padding: EdgeInsets.all(8.0),
            child: Text(' Ou entre com '),
          ),
          Expanded(
            child: Divider(thickness: 0.5),
          ),
        ],
      ),
    );
  }

  Row _getSocialRegisterButtons() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        SocialLoginButton(image: "apple", onPressed: _handleAppleRegister),
        const Gap(20),
        SocialLoginButton(image: "google", onPressed: _handleGoogleRegister),
      ],
    );
  }

  Row _getLoginButton() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        const Text("Já possui uma conta? "),
        InkWell(
          onTap: () => PageNavigator.goTo(NavigationPage.login),
          child: Text(
            "Faça login!",
            style: TextStyle(
              fontWeight: FontWeight.bold,
              color: Theme.of(context).colorScheme.secondary,
            ),
          ),
        ),
      ],
    );
  }

  void _handleRegister() async {
    String email = _emailController.text;

    List<String> parsedName = _nameController.text.split(' ');
    String firstName = parsedName[0];
    String lastName = parsedName[1];

    String rawBirthdate = _dateController.text;
    String birthdate = getFormattedDateInISO(rawBirthdate);

    Map<String, dynamic> userData = {
      'username': email,
      'firstName': firstName,
      'lastName': lastName,
      'email': email,
      'birthdate': birthdate,
    };

    PageNavigator.navigateTo(
      NavigationPage.createPassword,
      arguments: userData,
    );
  }

  void _handleGoogleRegister() async {
    // TODO: FIX

    // _pauseForRegister();

    // try {
    //   Map<String, dynamic> userData = await GoogleAPI.handleRegister();
    //   PageNavigator.goTo(NavigationPage.createPassword, arguments: userData);
    // } catch (err) {
    //   debugPrint('ERROR: Error signing in with google: $err');
    //   String errorMessage = 'Erro ao se registrar com o Google.';
    //   showGenericErrorDialog(message: errorMessage);
    //   _resumeAfterRegister();
    //   return;
    // }
  }

  void _handleAppleRegister() async {
    // TODO: IMPLEMENT
  }

  void _pauseForRegister() {
    _loadingOverlayKey.currentState?.pause();
  }

  void _resumeAfterRegister() {
    _loadingOverlayKey.currentState?.resume();
  }
}
