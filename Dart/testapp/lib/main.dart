// import 'package:flutter/material.dart';

// void main() {
//   runApp(MyApp());
// }

// abstract class AreaAbstract extends StatefulWidget {
//   const AreaAbstract({
//     Key? key,
//     required this.heightAbstract,
//     required this.widthAbstract,
//   }) : super(key: key);

//   final double heightAbstract;
//   final double widthAbstract;

//   Widget areaBuild();

//   @override
//   State<AreaAbstract> createState() => _AreaAbstractState();
// }

// class _AreaAbstractState extends State<AreaAbstract> {
//   double get height => widget.heightAbstract;
//   double get width => widget.widthAbstract;

//   @override
//   Widget build(BuildContext context) {
//     return Container(
//       width: width,
//       height: height,
//       color: const Color.fromARGB(0, 255, 193, 7),
//       padding: const EdgeInsets.symmetric(horizontal: 0),
//       child: SizedBox(
//         width: width,
//         height: height,
//         child: widget.areaBuild(),
//       ),
//     );
//   }
// }

// class ConcreteArea extends AreaAbstract {
//   ConcreteArea({Key? key, required double height, required double width})
//       : super(key: key, heightAbstract: height, widthAbstract: width);

//   int number = 0;

//   void increaseNumber() {
//     setState(() {
//       number++;
//     });
//   }

//   @override
//   Widget areaBuild() {
//     return Column(
//       mainAxisAlignment: MainAxisAlignment.center,
//       children: [
//         Text(
//           'Area: ${width * height}',
//           style: TextStyle(fontSize: 24),
//         ),
//         Text(
//           'Number: $number',
//           style: TextStyle(fontSize: 24),
//         ),
//         ElevatedButton(
//           onPressed: increaseNumber,
//           child: Text('Increase'),
//         ),
//       ],
//     );
//   }
// }

// class MyApp extends StatelessWidget {
//   @override
//   Widget build(BuildContext context) {
//     return MaterialApp(
//       title: 'Flutter Demo',
//       theme: ThemeData(
//         primarySwatch: Colors.blue,
//       ),
//       home: Scaffold(
//         appBar: AppBar(
//           title: Text('Abstract Area Demo'),
//         ),
//         body: Center(
//           child: ConcreteArea(
//             height: 200,
//             width: 150,
//           ),
//         ),
//       ),
//     );
//   }
// }
