import 'package:flutter/material.dart';
import 'package:http/http.dart';
import 'api_service.dart';
import 'signup.dart';
import 'snackbar_util.dart';
import 'home_screen.dart';
import 'package:provider/provider.dart';
import 'login_state_manager.dart';


class LogIn extends StatefulWidget {
  @override
  State<LogIn> createState() => _LogInState();
}

class _LogInState extends State<LogIn> {
  TextEditingController controller = TextEditingController();
  TextEditingController controller2 = TextEditingController();
  final apiService = ApiService();

  @override
  void initState() {
    super.initState();
    // Load the login state when the app starts
    Provider.of<LoginStateManager>(context, listen: false).loadLoginState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('로그인'),
        elevation: 0.0,
        backgroundColor: Colors.redAccent,
        centerTitle: true,
      ),
      
      body: GestureDetector(
        onTap: () {
          FocusScope.of(context).unfocus();
        },
        child: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Padding(padding: EdgeInsets.only(top: 50)),
              Center(
                child: Image(
                  image: AssetImage('assets/images/investrawberry.png'),
                  width: 170.0,
                ),
              ),
              
              Form(
                child: Theme(
                data: ThemeData(
                    primaryColor: Colors.grey,
                    inputDecorationTheme: InputDecorationTheme(
                        labelStyle: TextStyle(color: Colors.teal, fontSize: 15.0))),
                child: Container(
                    padding: EdgeInsets.all(40.0),
                    child: Builder(builder: (context) {
                      return Column(
                        children: [
                          TextField(
                            controller: controller,
                            autofocus: true,
                            decoration: InputDecoration(labelText: 'Enter email'),
                            keyboardType: TextInputType.emailAddress,
                          ),
                          TextField(
                            controller: controller2,
                            decoration:
                                InputDecoration(labelText: 'Enter password'),
                            keyboardType: TextInputType.text,
                            obscureText: true, // 비밀번호 안보이도록 하는 것
                          ),
                          SizedBox(
                            height: 40.0,
                          ),
                          TextButton(
                          onPressed: (){
                            // 회원가입 페이지로 이동
                            Navigator.push(
                              context,
                              MaterialPageRoute(builder: (context) => SignUpPage()),
                            );
                          },
                          child: Text(
                            '회원가입',
                            style: TextStyle(fontSize: 12),
                          ),
                          ),
                          ButtonTheme(
                              minWidth: 100.0,
                              height: 50.0,
                              child: ElevatedButton(
                                onPressed: () async {
                                  try {
                                    final jwtToken = 
                                      await apiService.login(controller.text, controller2.text);
                                      showSnackBar(context, Text('로그인 성공!'));
                                      final loginStateManager = Provider.of<LoginStateManager>(context, listen: false);
                                      loginStateManager.login(jwtToken);
                                      // 홈 화면으로 이동
                                      Navigator.push(
                                        context,
                                        MaterialPageRoute(
                                          builder: (context) => HomeScreen(),
                                        ),
                                      );
                                    print(jwtToken);
                                  } catch (e) {
                                    // 로그인이 실패한 경우 스낵바를 표시
                                    showSnackBar(context, Text('로그인 실패..'));
                                  }
                                },
                                child: Icon(
                                  Icons.arrow_forward,
                                  color: Colors.white,
                                  size: 35.0,
                                ),
                                style: ElevatedButton.styleFrom(
                                    backgroundColor: Colors.orangeAccent),
                              ))
                        ],
                      );
                    })),
              ))
            ],
          ),
        ),
      ),
    );
  }
}

