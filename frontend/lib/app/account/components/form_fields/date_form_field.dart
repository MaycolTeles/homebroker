import 'package:flutter/material.dart';
import 'package:frontend/core/components/form_fields/generic_form_field.dart';
import 'package:frontend/core/functions/datetime.dart';

class DateFormField extends StatefulWidget {
  final TextEditingController controller;
  final String labelText;

  const DateFormField({
    super.key,
    required this.controller,
    this.labelText = 'Data de Nascimento',
  });

  @override
  State<DateFormField> createState() => _DateFormFieldState();
}

class _DateFormFieldState extends State<DateFormField> {
  DateTime? _rawBirthDate;

  @override
  Widget build(BuildContext context) {
    // ColorScheme colorScheme = Theme.of(context).colorScheme;

    return GenericFormField(
      controller: widget.controller,
      labelText: widget.labelText,
      prefixIcon: Icons.calendar_month,
      validator: ((value) => _dateValidator(value)),
      onTap: () => _showDatePicker(context),
    );
  }

  void _showDatePicker(context) async {
    DateTime? date = await showDatePicker(
      context: context,
      locale: const Locale("pt", "BR"),
      helpText: "Selecione a data de nascimento",
      initialDate: DateTime.now(),
      firstDate: DateTime(1900),
      lastDate: DateTime.now(),
    );
    if (date == null) return;

    _rawBirthDate = date;
    String formattedDate = getFormattedDateInBRT(date);
    widget.controller.text = formattedDate.toString();
  }

  String? _dateValidator(String? date) {
    if (date!.isEmpty) {
      return "Por favor, insira uma data válida!";
    }

    if (!isAdult(_rawBirthDate!)) {
      return "Você deve ser maior de idade para se cadastrar!";
    }
    return null;
  }

  bool isAdult(DateTime dateTime) {
    DateTime now = DateTime.now();
    DateTime adult = DateTime(now.year - 18, now.month, now.day);
    return dateTime.isBefore(adult);
  }
}
