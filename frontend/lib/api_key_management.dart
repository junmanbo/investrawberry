import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'api_service.dart';
import 'login_state_manager.dart';

class ApiKeyRegistration extends StatefulWidget {
  @override
  _ApiKeyRegistrationState createState() => _ApiKeyRegistrationState();
}

class _ApiKeyRegistrationState extends State<ApiKeyRegistration> {
  final ApiService _apiService = ApiService();
  final _formKey = GlobalKey<FormState>();
  final _exchangeController = TextEditingController();
  final _accessKeyController = TextEditingController();
  final _secretKeyController = TextEditingController();
  final _accountNumberController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('API Key 등록'),
        elevation: 0.0,
        backgroundColor: Colors.redAccent,
        centerTitle: true,
      ),
      body: Form(
        key: _formKey,
        child: Padding(
          padding: EdgeInsets.all(16.0),
          child: Column(
            children: <Widget>[
              DropdownButtonFormField<String>(
                value: '선택',
                items: <String>['선택', '한국투자증권(국내)', '한국투자증권(해외)', '업비트'].map((String value) {
                  return DropdownMenuItem<String>(
                    value: value,
                    child: Text(value),
                  );
                }).toList(),
                onChanged: (value) {
                  switch (value) {
                    case '선택':
                      _exchangeController.text = '';
                      break;
                    case '한국투자증권(국내)':
                      _exchangeController.text = 'KIS_LOCAL';
                      break;
                    case '한국투자증권(해외)':
                      _exchangeController.text = 'KIS_INTL';
                      break;
                    case '업비트':
                      _exchangeController.text = 'UPBIT';
                      break;
                  }
                  //_exchangeController.text = value!;
                },
                decoration: InputDecoration(
                  labelText: '거래소',
                ),
                validator: (value) {
                  if (value == null || value.isEmpty || value == '선택') {
                    return '거래소를 선택해주세요.';
                  }
                  return null;
                },
              ),
              TextFormField(
                controller: _accessKeyController,
                decoration: InputDecoration(
                  labelText: '접근 키',
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return '접근 키를 입력해주세요.';
                  }
                  return null;
                },
              ),
              TextFormField(
                controller: _secretKeyController,
                decoration: InputDecoration(
                  labelText: '시크릿 키',
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return '시크릿 키를 입력해주세요.';
                  }
                  return null;
                },
              ),
              TextFormField(
                controller: _accountNumberController,
                decoration: InputDecoration(
                  labelText: '계좌번호',
                ),
              ),
              ElevatedButton(
                style: ElevatedButton.styleFrom(
                  primary: Colors.redAccent, // Set the color to redAccent
                ),
                onPressed: () {
                  if (_formKey.currentState!.validate()) {
                    _apiService.postExchangeKey(
                      Provider.of<LoginStateManager>(context, listen: false).jwtToken,
                      _exchangeController.text,
                      _accessKeyController.text,
                      _secretKeyController.text,
                      _accountNumberController.text,
                    );
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(content: Text('등록 되었습니다.')),
                    );
                    Navigator.pop(context, true); // Pass true to indicate that a key was added
                  }
                },
                child: Text('등록'),
              ),
              ElevatedButton(
                style: ElevatedButton.styleFrom(
                  primary: Colors.redAccent, // Set the color to redAccent
                ),
                onPressed: () {
                  Navigator.pop(context);
                },
                child: Text('취소'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class ApiKeyManagement extends StatefulWidget {
  @override
  _ApiKeyManagementState createState() => _ApiKeyManagementState();
}

class _ApiKeyManagementState extends State<ApiKeyManagement> {
  final ApiService _apiService = ApiService();

  Future<List<Map<String, dynamic>>> _getApiKeys(BuildContext context) async {
    return _apiService.getApiKeys(Provider.of<LoginStateManager>(context, listen: false).jwtToken);
  }

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
        future: _getApiKeys(context),
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
                      subtitle: Text(apiKey['access_key']?.substring(0, 4) ?? 'Unknown'),
                      trailing: IconButton(
                        icon: Icon(Icons.delete),
                        onPressed: () async {
                          await _apiService.deleteExchangeKey(Provider.of<LoginStateManager>(context, listen: false).jwtToken, apiKey['id']);
                          setState(() {}); // Refresh the state to update the list
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
        onPressed: () async {
          final result = await Navigator.push(
            context,
            MaterialPageRoute(builder: (context) => ApiKeyRegistration()),
          );
          if (result == true) {
            setState(() {});
          }
        },
      ),
    );
  }
}

