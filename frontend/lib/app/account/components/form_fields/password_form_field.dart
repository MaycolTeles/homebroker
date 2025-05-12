import 'package:flutter/material.dart';
import 'package:frontend/core/components/form_fields/generic_form_field.dart';

class PasswordFormField extends StatefulWidget {
  final TextEditingController controller;

  const PasswordFormField({
    super.key,
    required this.controller,
  });

  @override
  State<PasswordFormField> createState() => _PasswordFormFieldState();
}

class _PasswordFormFieldState extends State<PasswordFormField> {
  bool _obscureText = true;

  @override
  Widget build(BuildContext context) {
    Icon showPasswordIcon =
        Icon(_obscureText ? Icons.visibility : Icons.visibility_off);

    return GenericFormField(
      controller: widget.controller,
      obscureText: _obscureText,
      labelText: "Senha",
      validator: ((value) => _passwordValidator(value)),
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

  String? _passwordValidator(String? password) {
    bool isPasswordValid = password!.length >= 6;

    if (isPasswordValid) return null;

    // TODO: ADD PASSWORD VALIDATION
    return 'Por favor, insira uma senha válida! (mínimo de 6 caracteres)';
  }
}
