import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'api_service.dart';
import 'login_state_manager.dart';

class ApiKeyManagement extends StatelessWidget {
  final ApiService _apiService = ApiService();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('API Key 관리'),
        elevation: 0.0,
        backgroundColor: Colors.redAccent,
        centerTitle: true,
      ),
      body: FutureBuilder<List<Map<String, dynamic>>>(
        future: _apiService.getApiKeys(Provider.of<LoginStateManager>(context).jwtToken),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return CircularProgressIndicator(); // Show loading spinner while waiting for data
          } else if (snapshot.hasError) {
            return Text('Error: ${snapshot.error}'); // Show error message if there's an error
          } else {
            final apiKeys = snapshot.data ?? [];
            return apiKeys.isEmpty
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
                      title: Text(apiKey['exchange']['exchange_nm'] ?? 'Unknown'),
                      //subtitle: Text(apiKey['access_key'] ?? 'Unknown'),
                      subtitle: Text(apiKey['access_key']?.substring(0, 10) ?? 'Unknown'),
                      trailing: IconButton(
                        icon: Icon(Icons.delete),
                        onPressed: () {
                          // TODO: Implement delete functionality
                        },
                      ),
                    );
                  },
                );
          }
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

