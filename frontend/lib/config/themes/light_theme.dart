import 'package:flutter/material.dart';
import 'package:frontend/config/themes/colors.dart';
import 'package:google_fonts/google_fonts.dart';

TextTheme _textTheme = GoogleFonts.interTextTheme();
TextTheme _primaryTextTheme = GoogleFonts.modakTextTheme();

const Color _primaryColor = Color(0xFF1976D2);
const Color _secondaryColor = Color(0xFF43A047);
const Color _tertiaryColor = Color(0xFFE53935);
const Color _backgroundColor = Color(0XFFF5F5F5);
const Color _textColor = Color(0xFF212121);

const ColorScheme _colorScheme = ColorScheme.light();

ThemeData lightThemeData = ThemeData.from(colorScheme: _colorScheme).copyWith(
  primaryColor: _primaryColor,
  secondaryHeaderColor: _secondaryColor,
  scaffoldBackgroundColor: _backgroundColor,
  textTheme: _textTheme.apply(
    bodyColor: _textColor,
    displayColor: _textColor,
  ),
  primaryTextTheme: _primaryTextTheme.apply(
    // bodyColor: _secondaryColor,
    displayColor: _secondaryColor,
  ),
  buttonTheme: const ButtonThemeData(
    buttonColor: _primaryColor,
    // textTheme: ButtonTextTheme.normal,
  ),
  elevatedButtonTheme: ElevatedButtonThemeData(
    style: ElevatedButton.styleFrom(
      foregroundColor: Colors.white,
      backgroundColor: _primaryColor,
    ),
  ),
  colorScheme: const ColorScheme.highContrastLight().copyWith(
    primary: _primaryColor,
    secondary: _secondaryColor,
    tertiary: _tertiaryColor,
    outline: mainBlack,
  ),
  iconTheme: const IconThemeData(
    color: _secondaryColor,
  ),
  appBarTheme: const AppBarTheme(
    backgroundColor: _primaryColor,
  ),
  bottomNavigationBarTheme: BottomNavigationBarThemeData(
    selectedItemColor: _primaryColor,
    unselectedItemColor: _primaryColor,
    selectedLabelStyle: TextStyle(color: _primaryColor),
    unselectedLabelStyle: TextStyle(color: _primaryColor),
    // selectedIconTheme: IconThemeData(color: _primaryColor),
    // unselectedIconTheme: IconThemeData(color: _primaryColor),
  ),
  cardTheme: CardTheme(
    color: _primaryColor,
  ),
  floatingActionButtonTheme: const FloatingActionButtonThemeData(
    backgroundColor: _primaryColor,
  ),
);
