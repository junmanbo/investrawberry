import 'package:flutter/material.dart';
import 'my_page.dart';

class HomeScreen extends StatefulWidget {
  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _selectedIndex = 0;

  static List<Widget> _widgetOptions = [
    Center(
      child: Image.asset('assets/images/investrawberry.png', width: 170.0),
    ),
    Text('자산'),
    Text('전략'),
    MyPage(),
  ];

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(['Investrawberry','자산','전략','MY'][_selectedIndex]),
        elevation: 0.0,
        backgroundColor: Colors.redAccent,
        centerTitle: false,
      ),
      body: Center(
        child: _widgetOptions.elementAt(_selectedIndex),
      ),
      bottomNavigationBar: BottomNavigationBar(
        items: const <BottomNavigationBarItem>[
          BottomNavigationBarItem(
            icon: Icon(Icons.home),
            label: '홈',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.attach_money),
            label: '자산',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.show_chart),
            label: '전략',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.person),
            label: 'MY',
          ),
        ],
        currentIndex: _selectedIndex,
        selectedItemColor: Colors.redAccent,
        unselectedItemColor: Colors.grey.shade400,
        onTap: _onItemTapped,
      ),
    );
  }
}

