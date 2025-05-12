import 'package:flutter/material.dart';
import 'package:frontend/core/components/form_fields/generic_form_field.dart';

class PasswordConfirmationFormField extends StatefulWidget {
  final TextEditingController passwordController;
  final TextEditingController passwordConfirmationController;

  const PasswordConfirmationFormField({
    super.key,
    required this.passwordController,
    required this.passwordConfirmationController,
  });

  @override
  State<PasswordConfirmationFormField> createState() =>
      PasswordConfirmationFormFieldState();
}

class PasswordConfirmationFormFieldState
    extends State<PasswordConfirmationFormField> {
  bool _obscureText = true;

  @override
  Widget build(BuildContext context) {
    Icon showPasswordIcon =
        Icon(_obscureText ? Icons.visibility : Icons.visibility_off);

    return GenericFormField(
      controller: widget.passwordConfirmationController,
      obscureText: _obscureText,
      validator: ((value) => passwordConfirmationValidator()),
      labelText: "Confirme a senha",
      prefixIcon: Icons.lock,
      suffixIcon: IconButton(
        onPressed: () => _togglePasswordVisibility(),
        icon: showPasswordIcon,
        color: Theme.of(context).iconTheme.color,
      ),
    );
  }

  void _togglePasswordVisibility() {
    setState(() => _obscureText = !_obscureText);
  }

  String? passwordConfirmationValidator() {
    bool passwordsMatch = _validateMatchingPasswords();

    if (passwordsMatch) return null;

    return 'As senhas não coincidem';
  }

  bool _validateMatchingPasswords() {
    String password = widget.passwordController.text;
    String passwordConfirmation = widget.passwordConfirmationController.text;

    bool passwordsMatch = password == passwordConfirmation;
    return passwordsMatch;
  }
}
