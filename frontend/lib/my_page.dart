import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'login_state_manager.dart';
import 'login.dart';
import 'api_key_management.dart';

class MyPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final loginStateManager = Provider.of<LoginStateManager>(context);
    final isLoggedIn = loginStateManager.isLoggedIn;

    return Scaffold(
      body: Center(
        child: isLoggedIn ? loggedInWidget(context, loginStateManager) : notLoggedInWidget(context),
      ),
    );
  }

  Widget loggedInWidget(BuildContext context, LoginStateManager loginStateManager) {
    return FutureBuilder<Map<String, dynamic>>(
      future: loginStateManager.getUserInfo(),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return CircularProgressIndicator();
        } else if (snapshot.hasError) {
          return Text('Error: ${snapshot.error}');
        } else {
          final userInfo = snapshot.data;
          if (userInfo != null) {
            final fullName = userInfo['full_name'];
            return Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Text('$fullName 님 환영합니다!'),
                SizedBox(height: 16),
                ElevatedButton(
                  onPressed: () {
                    // API Key 관리 페이지로 이동
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                    builder: (context) => ApiKeyManagement(),
                      ),
                    );
                  },
                  child: Text('API Key 관리'),
                  style: ElevatedButton.styleFrom(
                    primary: Colors.redAccent,
                  ),
                ),
                SizedBox(height: 16),
                ElevatedButton(
                  onPressed: () {
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

          } else {
            return Text('유저 정보를 불러오는 데 실패했습니다.');
          }
        }
      },
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

