import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'login_state_manager.dart';
import 'login.dart';
// API Key 관리 페이지를 import 하세요.
// import 'api_key_management.dart';

class MyPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {

    final isLoggedIn = Provider.of<LoginStateManager>(context).isLoggedIn;

    return Scaffold(
      body: Center(
        child: isLoggedIn ? loggedInWidget(context) : notLoggedInWidget(context),
      ),
    );
  }

  Widget loggedInWidget(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        Text('OOO 님 환영합니다!'),
        SizedBox(height: 16),
        ElevatedButton(
          onPressed: () {
            // API Key 관리 페이지로 이동하는 코드를 작성하세요.
            // Navigator.push(
            //   context,
            //   MaterialPageRoute(
            //     builder: (context) => ApiKeyManagement(),
            //   ),
            // );
          },
          child: Text('API Key 관리'),
          style: ElevatedButton.styleFrom(
            primary: Colors.redAccent,
          ),
        ),
        SizedBox(height: 16),
        // 로그아웃 기능 구현 위치에 로그아웃 메소드 호출 코드를 추가하세요.
        ElevatedButton(
          onPressed: () {
            final loginStateManager = Provider.of<LoginStateManager>(context, listen: false);
            loginStateManager.logout(); 
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => LogIn(),
              ),
            );
          },
          child: Text('로그아웃'),
          style: ElevatedButton.styleFrom(
            primary: Colors.redAccent,
          ),
        ),
      ],
    );
  }

  Widget notLoggedInWidget(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        Text('로그인이 필요한 서비스입니다.'),
        SizedBox(height: 16),
        ElevatedButton(
          onPressed: () {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => LogIn(),
              ),
            );
          },
          child: Text('로그인'),
          style: ElevatedButton.styleFrom(
            primary: Colors.redAccent,
          ),
        ),
      ],
    );
  }
}

