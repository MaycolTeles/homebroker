import 'package:flutter/material.dart';
import 'package:frontend/core/functions/logo.dart';

class SocialLoginButton extends StatelessWidget {
  final String image;
  final VoidCallback onPressed;

  const SocialLoginButton({
    super.key,
    required this.image,
    required this.onPressed,
  });

  @override
  Widget build(BuildContext context) {
    Color secondaryColor = Theme.of(context).colorScheme.secondary;

    return GestureDetector(
      onTap: () => onPressed,
      child: Container(
        padding: const EdgeInsets.all(20.0),
        decoration: BoxDecoration(
          border: Border.all(
            color: secondaryColor,
            width: 2.0,
          ),
          borderRadius: BorderRadius.circular(16.0),
        ),
        child: Image.asset(
          getImagePath('assets/images/logos/$image.png'),
          height: 20,
        ),
      ),
    );
  }
}
