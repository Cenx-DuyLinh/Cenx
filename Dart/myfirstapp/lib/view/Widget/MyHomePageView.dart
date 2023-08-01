import 'package:flutter/material.dart';
import 'package:myfirstapp/view/Text/TestText.dart';
class MyHomePage extends StatelessWidget {
  const MyHomePage({super.key});

  @override
  Widget build(BuildContext context) {
      return Scaffold(
        backgroundColor: Colors.amber,
        appBar: AppBar(
          title: const TestText(input: 'Hello world'),
        ),
      
      );
  //   return Scaffold(
  //     backgroundColor: Color.fromARGB(255, 10, 17, 31),
  //     appBar: AppBar(
  //       title: Row(
  //         children: [
  //           TextButton(
  //             onPressed: (){print('Hello');},
  //             style: ButtonStyle(
  //               overlayColor: MaterialStateProperty.all(Colors.transparent)
  //             ),
  //             child: RichText(
  //               text: const TextSpan(
  //                 children: [
  //                   TextSpan(
  //                     text: 'Studio',
  //                     style: TextStyle(fontWeight: FontWeight.bold,fontSize: 35, color: Color.fromARGB(255, 255, 255, 255)),
  //                   ),
  //                   TextSpan(
  //                     text: 'UI',
  //                     style: TextStyle(fontWeight: FontWeight.bold,fontSize: 35, color: Color.fromARGB(255, 46, 54, 143)),
  //                   ),
  //                 ]
  //               ),
  //             ),
  //           ),
  //           TextButton(
  //             onPressed: (){},
  //             child: const Text('Pressed me'),
  //           ),
  //         ],
  //       ),
  //       actions: <Widget>[
  //         IconButton(
  //           onPressed: () {},
  //           icon: const Icon(Icons.search),
  //   ),
  //         IconButton(
  //           onPressed: () {},
  //           icon: const Icon(Icons.notifications),
  //   ),
  // ],
  //       backgroundColor: const Color.fromARGB(0, 0, 0, 0),
  //     ),
  //   );
  }
}