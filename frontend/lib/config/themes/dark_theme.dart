import 'package:flutter/material.dart';
import 'package:frontend/config/themes/colors.dart';
import 'package:google_fonts/google_fonts.dart';

TextTheme _textTheme = GoogleFonts.interTextTheme();
TextTheme _primaryTextTheme = GoogleFonts.modakTextTheme();

const Color _primaryColor = Color(0xFF90CAF9);
const Color _secondaryColor = Color(0xFF66BB6A);
const Color _tertiaryColor = Color(0xFFEF5350);
const Color _backgroundColor = mainBlack5;
const Color _textColor = Color(0xFFE0E0E0);
// const Color _primaryColorLighter = Color(0xFF732FA3); // TODO: RENOMEAR

const ColorScheme _colorScheme = ColorScheme.dark();

ThemeData darkThemeData = ThemeData.from(colorScheme: _colorScheme).copyWith(
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
      foregroundColor: Colors.black,
      backgroundColor: _primaryColor,
    ),
  ),
  colorScheme: const ColorScheme.highContrastDark().copyWith(
    primary: _primaryColor,
    secondary: _secondaryColor,
    tertiary: _tertiaryColor,
    outline: Colors.white,
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
