import 'package:flutter/material.dart';

class GenericFormField extends StatefulWidget {
  final TextEditingController controller;
  final TextInputType keyboardType;
  final bool obscureText;
  final String hintText;
  final String labelText;
  final InputBorder border;
  final String? Function(String?)? validator;
  final void Function()? onTap;
  final IconData? prefixIcon;
  final Widget? suffixIcon;

  const GenericFormField({
    super.key,
    required this.controller,
    this.keyboardType = TextInputType.text,
    this.obscureText = false,
    this.hintText = "",
    this.labelText = "",
    this.border = const OutlineInputBorder(
      borderRadius: BorderRadius.all(Radius.circular(8.0)),
    ),
    this.validator = _textValidator,
    this.onTap,
    this.suffixIcon,
    this.prefixIcon,
  });

  @override
  State<GenericFormField> createState() => _GenericFormFieldState();
}

class _GenericFormFieldState extends State<GenericFormField> {
  @override
  Widget build(BuildContext context) {
    return TextFormField(
      controller: widget.controller,
      keyboardType: widget.keyboardType,
      obscureText: widget.obscureText,
      validator: widget.validator,
      onTap: widget.onTap,
      decoration: InputDecoration(
        errorMaxLines: 2,
        hintText: widget.hintText,
        labelText: widget.labelText,
        border: widget.border,
        prefixIcon: _getPrefixIconIfExists(),
        suffixIcon: _getSuffixIconIfExists(),
      ),
    );
  }

  Widget? _getPrefixIconIfExists() {
    if (widget.prefixIcon == null) {
      return null;
    }

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16.0),
      child: Icon(
        widget.prefixIcon,
        color: Theme.of(context).iconTheme.color,
      ),
    );
  }

  Widget? _getSuffixIconIfExists() {
    if (widget.suffixIcon == null) {
      return null;
    }

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16.0),
      child: widget.suffixIcon,
    );
  }
}

String? _textValidator(String? text) {
  if (text!.isEmpty) {
    return "Por favor, insira um valor válido!";
  }
  return null;
}
