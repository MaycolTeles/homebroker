import 'package:flutter/material.dart';
import 'package:frontend/core/components/buttons/generic_elevated_button.dart';

class RectangularButton extends StatelessWidget {
  final String text;
  final VoidCallback onPressed;
  final Size minimumSize;

  const RectangularButton({
    super.key,
    required this.text,
    required this.onPressed,
    this.minimumSize = const Size(120, 60),
  });

  @override
  Widget build(BuildContext context) {
    return GenericElevatedButton(
      text: text,
      onPressed: onPressed,
      style: ElevatedButton.styleFrom(
        minimumSize: minimumSize,
        elevation: 10,
        shape: const RoundedRectangleBorder(
          borderRadius: BorderRadius.all(
            Radius.circular(8.0),
          ),
        ),
      ),
    );
  }
}
