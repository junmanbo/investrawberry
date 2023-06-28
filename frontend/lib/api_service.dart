import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = 'http://127.0.0.1:8000/api/v1';

  Future<String> login(String email, String password) async {
    final response = await _post('$baseUrl/login/access-token', {'username': email, 'password': password});
    return response['access_token'];
  }

  Future<Map<String, dynamic>> getUserInfo(String token) async {
    final response = await _get('$baseUrl/users/me', {'Content-Type': 'application/json', 'Authorization': 'Bearer $token'});
    return response;
  }

  Future<bool> signUp(String email, String password, String fullname) async {
    final response = await _post(
      '$baseUrl/users/open',
      {'email': email, 'password': password, 'full_name': fullname},
      headers: {'Content-Type': 'application/json'},
    );

    if (response != null) {
      print('회원가입 완료');
      return true;
    } else {
      print('회원가입 실패, 응답 본문: ${response.toString()}'); // 응답 본문 출력
      return false;
    }
  }

  Future<List<Map<String, dynamic>>> getApiKeys(String token) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/exchangekeys/'),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $token',
        },
      );

      _checkStatusCode(response.statusCode);

      return List<Map<String, dynamic>>.from(jsonDecode(response.body));
    } catch (e) {
      throw Exception('Failed to load API keys: $e');
    }
  }

  Future<void> postExchangeKey(String token, String exchange, String accessKey, String secretKey, String accountNumber) async {
    final url = '$baseUrl/exchangekeys/';
    final headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer $token',
    };
    final body = {
      'exchange_nm': exchange,
      'exchange_key_in': {
        'access_key': accessKey,
        'secret_key': secretKey,
        'account': accountNumber,
      },
    };
    try {
      final response = await _post(url, body, headers: headers);
      print('Exchange key posted successfully');
    } on Exception catch (e) {
      print('Failed to post exchange key: $e');
      throw e;
    }
}

  Future<void> deleteExchangeKey(String token, int exchangeKeyId) async {
    final url = '$baseUrl/exchangekeys/$exchangeKeyId';
    final headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer $token'};
    try {
      final response = await _delete(url, headers);
      print('Exchange key deleted successfully');
    } on Exception catch (e) {
      print('Failed to delete exchange key: $e');
    }
  }

  // method
  Future<Map<String, dynamic>> _get(String url, Map<String, String> headers) async {
    try {
      final response = await http.get(Uri.parse(url), headers: headers);
      _checkStatusCode(response.statusCode);
      return jsonDecode(response.body);
    } catch (e) {
      throw Exception('Failed to GET $url: $e');
    }
  }

  Future<Map<String, dynamic>> _post(String url, Map<String, dynamic> body, {Map<String, String> headers = const {}}) async {
    try {
      //final response = await http.post(Uri.parse(url), headers: headers, body: jsonEncode(body));
      final response = await http.post(Uri.parse(url), headers: headers, body: url.contains('/login/access-token') ? body : jsonEncode(body));
      _checkStatusCode(response.statusCode);
      return jsonDecode(response.body);
    } catch (e) {
      throw Exception('Failed to POST $url: $e');
    }
  }

  Future<Map<String, dynamic>> _delete(String url, Map<String, String> headers) async {
    try {
      final response = await http.delete(Uri.parse(url), headers: headers);
      _checkStatusCode(response.statusCode);
      return jsonDecode(response.body);
    } catch (e) {
      throw Exception('Failed to DELETE $url: $e');
    }
  }

  void _checkStatusCode(int statusCode) {
    if (statusCode < 200 || statusCode >= 300) {
      throw Exception('Failed with status code: $statusCode');
    }
  }
}

