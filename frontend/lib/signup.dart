import 'package:flutter/material.dart';
import 'api_service.dart';
import 'snackbar_util.dart';

class SignUpPage extends StatefulWidget {
  @override
  _SignUpPageState createState() => _SignUpPageState();
}

class _SignUpPageState extends State<SignUpPage> {
  TextEditingController _emailController = TextEditingController();
  TextEditingController _passwordController = TextEditingController();
  TextEditingController _rePasswordController = TextEditingController();
  TextEditingController _fullnameController = TextEditingController();
  final apiService = ApiService();

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    _rePasswordController.dispose();
    _fullnameController.dispose();


    super.dispose();
  }

  void _signUp() async {
    String email = _emailController.text.trim();
    String password = _passwordController.text.trim();
    String rePassword = _rePasswordController.text.trim();
    String fullname = _fullnameController.text.trim(); // 이름 추가

    // 이메일, 비밀번호, 비밀번호 확인, 이름 유효성 검사
    if (email.isEmpty || password.isEmpty || rePassword.isEmpty || fullname.isEmpty) {
      showSnackBar(context, Text('이메일, 비밀번호, 비밀번호 확인, 이름은 필수 항목입니다.'));
      return;
    }
    if (password != rePassword) {
      showSnackBar(context, Text('비밀번호가 일치하지 않습니다.'));
      return;
    }

    try {
      bool signupSuccess = await apiService.signUp(email, password, fullname);
      if (signupSuccess) {
        showDialog(
          context: context,
          builder: (BuildContext context) {
            return AlertDialog(
              title: Text('회원가입 성공'),
              content: Text('확인 버튼을 눌러 로그인 페이지로 이동하세요.'),
              actions: <Widget>[
                TextButton(
                  onPressed: () {
                    Navigator.pop(context); // 팝업을 닫습니다.
                    Navigator.pop(context); // 로그인 페이지로 이동합니다.
                  },
                  child: Text('확인'),
                ),
              ],
            );
          }
        );
      } else {
        showSnackBar(context, Text('회원가입에 실패했습니다.'));
      }
    } catch (e) {
      showSnackBar(context, Text('회원가입 중 오류가 발생했습니다. 다시 시도해주세요.'));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: Text('회원가입'),
          backgroundColor: Colors.redAccent,
        ),
        body: Padding(
          padding: EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              TextField(
                controller: _emailController,
                decoration: InputDecoration(labelText: '이메일'),
              ),
              TextField(
                controller: _passwordController,
                decoration: InputDecoration(labelText: '비밀번호'),
                obscureText: true,
              ),
              TextField(
                controller: _rePasswordController,
                decoration: InputDecoration(labelText: '비밀번호 확인'),
                obscureText: true,
              ),
              TextField(
                controller: _fullnameController,
                decoration: InputDecoration(labelText: '이름'),
              ),
              ElevatedButton(
                onPressed: () {
                  // 회원가입 API 호출 및 유효성 검증 로직 추가
                  _signUp();
                },
                child: Text('회원가입'),
                style: ElevatedButton.styleFrom(
                  primary: Colors.redAccent,
                ),
              ),
            ],
          ),
        ));
  }
}

