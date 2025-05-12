import 'package:flutter/material.dart';
import 'package:frontend/core/components/form_fields/generic_form_field.dart';
// import 'package:frontend/styles/colors.dart';

class CustomFormField extends StatelessWidget {
  final TextEditingController controller;
  final String labelText;
  final IconData? prefixIcon;

  const CustomFormField({
    super.key,
    required this.controller,
    this.labelText = "",
    this.prefixIcon = Icons.person,
  });

  @override
  Widget build(BuildContext context) {
    // ColorScheme colorScheme = Theme.of(context).colorScheme;

    return GenericFormField(
      controller: controller,
      labelText: labelText,
      prefixIcon: prefixIcon,
    );
  }
}
