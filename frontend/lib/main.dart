import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'login_state_manager.dart';
import 'home_screen.dart';
import 'login.dart';
import 'my_page.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (context) => LoginStateManager(),
      child: MaterialApp(
        debugShowCheckedModeBanner: false,
        title: 'Investroberry',
        home: HomeScreen(),
      ),
    );
  }
}

// class MyHomePage extends StatelessWidget {
//   @override
//   Widget build(BuildContext context) {
//     return DefaultTabController(
//       length: 2,
//       child: Scaffold(
//         appBar: AppBar(
//           title: Text('Investroberry'),
//           bottom: TabBar(
//             tabs: [
//               Tab(icon: Icon(Icons.lock_open_outlined), text: '로그인'),
//               Tab(icon: Icon(Icons.person), text: 'MY'),
//             ],
//           ),
//         ),
//         body: TabBarView(
//           children: [
//             LogIn(),
//             MyPage(),
//           ],
//         ),
//       ),
//     );
//   }
// }
//
//
