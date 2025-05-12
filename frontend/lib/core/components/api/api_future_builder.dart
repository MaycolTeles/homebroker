import 'package:flutter/material.dart';

class APIFutureBuilder<T> extends StatelessWidget {
  final Future<T> future;
  final Widget Function(T data) builder;
  final String errorMessage;
  final String emptyDataMessage;

  const APIFutureBuilder({
    super.key,
    required this.future,
    required this.builder,
    this.errorMessage = 'Erro ao carregar dados',
    this.emptyDataMessage = 'Nenhum dado encontrado',
  });

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<T>(
      future: future,
      builder: (context, snapshot) {
        final data = snapshot.data;

        bool isWaiting = snapshot.connectionState == ConnectionState.waiting;
        bool hasNoData = data == null || (data is List && data.isEmpty);

        if (isWaiting) return _getLoader();
        if (snapshot.hasError) return _getErrorMessage();
        if (hasNoData) return _getEmptyDataMessage();

        return builder(data);
      },
    );
  }

  Center _getLoader() {
    return const Center(
      child: CircularProgressIndicator(),
    );
  }

  Center _getErrorMessage() {
    return Center(
      child: Text(errorMessage),
    );
  }

  Center _getEmptyDataMessage() {
    return Center(
      child: Text(emptyDataMessage),
    );
  }
}
