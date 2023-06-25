import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'api_service.dart';

class LoginStateManager with ChangeNotifier {
  bool _isLoggedIn = false;
  String _jwtToken = '';
  ApiService _apiService = ApiService();

  bool get isLoggedIn => _isLoggedIn;
  String get jwtToken => _jwtToken;

  Future<void> login(String token) async {
    _isLoggedIn = true;
    _jwtToken = token;

    // Save the token in shared preferences
    SharedPreferences prefs = await SharedPreferences.getInstance();
    await prefs.setString('jwtToken', token);

    notifyListeners();
  }

  Future<void> loadLoginState() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();

    // Load the token from shared preferences
    _jwtToken = prefs.getString('jwtToken') ?? '';
    _isLoggedIn = _jwtToken.isNotEmpty;

    notifyListeners();
  }

  Future<void> logout() async {
    _isLoggedIn = false;
    _jwtToken = '';

    // Remove the token from shared preferences
    SharedPreferences prefs = await SharedPreferences.getInstance();
    await prefs.remove('jwtToken');

    notifyListeners();
  }

  Future<Map<String, dynamic>> getUserInfo() async {
    if (_isLoggedIn) {
      return await _apiService.getUserInfo(_jwtToken);
    } else {
      throw Exception('Not logged in.');
    }
  }
}

