import 'package:flutter/material.dart';

class LoadingOverlay extends StatefulWidget {
  final Scaffold scaffold;

  const LoadingOverlay({
    super.key,
    required this.scaffold,
  });

  @override
  State<LoadingOverlay> createState() => LoadingOverlayState();
}

class LoadingOverlayState extends State<LoadingOverlay> {
  bool _isLoading = false;

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        widget.scaffold,
        if (_isLoading)
          ModalBarrier(
            color: Colors.black.withOpacity(0.5),
            dismissible: false,
          ),
        if (_isLoading)
          const Center(
            child: CircularProgressIndicator(),
          ),
      ],
    );
  }

  void pause() {
    setState(() => _isLoading = true);
  }

  void resume() {
    setState(() => _isLoading = false);
  }
}
