import 'package:email_validator/email_validator.dart';
import 'package:flutter/material.dart';
import 'package:frontend/core/components/form_fields/generic_form_field.dart';

class EmailFormField extends StatelessWidget {
  final TextEditingController controller;

  const EmailFormField({
    super.key,
    required this.controller,
  });

  @override
  Widget build(BuildContext context) {
    return GenericFormField(
      controller: controller,
      labelText: "E-mail",
      keyboardType: TextInputType.emailAddress,
      validator: _emailValidator,
      prefixIcon: Icons.email,
    );
  }

  String? _emailValidator(String? email) {
    if (!EmailValidator.validate(email!)) {
      return "Por favor, insira um e-mail válido!";
    }
    return null;
  }
}
