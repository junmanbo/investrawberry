import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = 'http://127.0.0.1:8000/api/v1';

  Future<String> login(String email, String password) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/login/access-token'),
        body: {'username': email, 'password': password},
      );

      if (response.statusCode == 200) {
        final jsonResponse = jsonDecode(response.body);
        final accessToken = jsonResponse['access_token'];
        return accessToken;
      } else {
        throw Exception('Failed to log in.');
      }
    } catch (e) {
      throw Exception(e.toString());
    }
  }
  Future<bool> signUp(String email, String password, String fullname) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/users/open'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'email': email, 
          'password': password, 
          'full_name': fullname
        }),
      );

      if (response.statusCode == 200) {
        print('회원가입 완료');
        return true;
      } else {
        print('회원가입 실패, 응답 본문: ${response.body}'); // 응답 본문 출력
        return false;
      }
    } catch (e) {
      throw Exception(e.toString());
    }
  }
}

