import 'package:intl/intl.dart';

/// Format date and time from yyyy-MM-dd HH:mm:ss to dd/MM/yyyy HH:mm
String getFormattedDateTimeInBRT(DateTime date) {
  return DateFormat('dd/MM/yyyy HH:mm').format(date);
}

/// Format date from yyyy-MM-dd to dd/MM/yyyy
String getFormattedDateInBRT(DateTime date) {
  return DateFormat('dd/MM/yyyy').format(date);
}

/// Format date from dd/MM/yyyy to yyyy-MM-dd
String getFormattedDateInISO(String date) {
  String day = date.substring(0, 2);
  String month = date.substring(3, 5);
  String year = date.substring(6);

  return "$year-$month-$day";
}
