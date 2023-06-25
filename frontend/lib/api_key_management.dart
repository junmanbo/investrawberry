import 'package:flutter/material.dart';

class ApiKeyManagement extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    // TODO: Replace this with your actual data
    final apiKeys = [
      {'exchange': 'Binance', 'accessKey': '123456'},
      {'exchange': 'Coinbase', 'accessKey': '789012'},
    ];

    return Scaffold(
      appBar: AppBar(
        title: Text('API Key 관리'),
        elevation: 0.0,
        backgroundColor: Colors.redAccent,
        centerTitle: true,
      ),
      body: apiKeys.isEmpty
          ? Center(
              child: Text(
                '등록된 API Key 가 없습니다. 아래의 + 버튼을 눌러 Key를 추가해 주세요.',
              ),
            )
          : ListView.builder(
              itemCount: apiKeys.length,
              itemBuilder: (context, index) {
                final apiKey = apiKeys[index];
                return ListTile(
                  leading: Image.asset('assets/images/logo.png'), // Replace with your actual logo image
                  title: Text(apiKey['exchange'] ?? 'Unknown'),
                  subtitle: Text(apiKey['accessKey'] ?? 'Unknown'),
                  trailing: IconButton(
                    icon: Icon(Icons.delete),
                    onPressed: () {
                      // TODO: Implement delete functionality
                    },
                  ),
                );
              },
            ),
      floatingActionButton: FloatingActionButton(
        child: Icon(Icons.add),
        backgroundColor: Colors.redAccent, // Same color as AppBar
        onPressed: () {
          // TODO: Implement add functionality
        },
      ),
    );
  }
}

