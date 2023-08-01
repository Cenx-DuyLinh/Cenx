import 'package:flutter/material.dart';

class MyTestWidget extends StatelessWidget {
  const MyTestWidget({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Color.fromRGBO(195, 59, 59, 1),
        title: const Text('Register'),
      ),
      body: Center(
        child: TextButton(
          onPressed: (){
            print('hello');
          },
          child: const Text('Registered')
        ),
      ),
    );
  }
}