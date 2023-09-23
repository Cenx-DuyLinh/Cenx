// // ignore_for_file: avoid_print, unused_import

// import 'package:flutter/material.dart';
// import 'package:my_app/view/widgets/widgets_studioui/widgets_components/FirstSectionWidget.dart';
// import '../../widgets_components/AppBarWidget.dart';
// import '../../widgets_components/PaddingWidget.dart';
// import 'package:my_app/view/factories/AreaAbstract.dart';
// import 'package:my_app/viewmodel/test_ui_viewmodel.dart';
// import 'dart:convert';
// import 'dart:io';
// import 'package:flutter/services.dart'; //Have root bundle and unit 8 bit
// import 'package:path/path.dart' as path;
// import 'package:file_picker/file_picker.dart';

// // import 'package:my_app/view/widgets/widgets_studioui/widgets_components/PaddingWidget.dart';
// class PlaceHolderDummy extends StatefulWidget {
//   final double widthAbstract;
//   final double heightAbstract;
//   const PlaceHolderDummy(
//       {super.key, required this.widthAbstract, required this.heightAbstract});

//   @override
//   State<PlaceHolderDummy> createState() => _PlaceHodlerDummyState();
// }

// class _PlaceHodlerDummyState extends State<PlaceHolderDummy> {
//   //!Will implement this in a class later, hopefully..
//   String userName = '';
//   String passWord = '';
//   String email = '';
//   File? imageFile;
//   String url = '';
//   //!--------------[Login Method]----------------
//   dynamic _getLoginData() {
//     dynamic data = {"username": userName, "password": passWord, "email": email};
//     return data;
//   }

//   //!--------------[Get Image Method]----------------
//   dynamic _getImageData(imageBase64) {
//     dynamic data = {
//       'FileName': 'asset_frontpageguy.png',
//       'FileContent': imageBase64,
//     };
//     return data;
//   }

//   Future<Uint8List> loadAsset(String assetPath) async {
//     final data = await rootBundle.load(assetPath);
//     return data.buffer.asUint8List();
//   }

//   //!--------------[Upload Image Method]----------------

//   Future _openFileExplorer() async {
//     try {
//       FilePickerResult? result = await FilePicker.platform.pickFiles(
//         type: FileType.custom,
//         allowedExtensions: ['jpg', 'png'],
//       );

//       Uint8List? bytes = result?.files.single.bytes;
//       if (bytes != null) {
//         return base64Encode(bytes);
//       } else {
//         print('Error: The picked file has no bytes.');
//       }
//     } catch (e) {
//       print('Error picking image: $e');
//     }
//   }

// //!--------------[Widget Build]---------------------
//   @override
//   Widget build(BuildContext context) {
//     return SizedBox(
//       width: widget.widthAbstract,
//       height: widget.heightAbstract,
//       child: Column(
//         children: [
//           TextField(
//             style: const TextStyle(
//               color: Colors.white,
//               fontSize: 20,
//               fontWeight: FontWeight.bold,
//             ),
//             onChanged: (value) {
//               setState(() {
//                 userName = value;
//               });
//             },
//             decoration: const InputDecoration(
//                 labelText: 'User Name: ',
//                 labelStyle: TextStyle(
//                   color: Colors.white,
//                 )),
//           ),
//           TextField(
//             style: const TextStyle(
//               color: Colors.white,
//               fontSize: 20,
//               fontWeight: FontWeight.bold,
//             ),
//             onChanged: (value) {
//               setState(() {
//                 passWord = value;
//               });
//             },
//             decoration: const InputDecoration(
//                 labelText: 'Password: ',
//                 labelStyle: TextStyle(
//                   color: Colors.white,
//                 )),
//           ),
//           TextField(
//             style: const TextStyle(
//               color: Colors.white,
//               fontSize: 20,
//               fontWeight: FontWeight.bold,
//             ),
//             onChanged: (value) {
//               setState(() {
//                 email = value;
//               });
//             },
//             decoration: const InputDecoration(
//                 labelText: 'Email: ',
//                 labelStyle: TextStyle(
//                   color: Colors.white,
//                 )),
//           ),
//           const SmallVerticalPadding(),
//           ElevatedButton(
//             onPressed: () {
//               //!-------------[IMPORTANT STUFF]------------------------------------------------------
//               TestUIModel().post('/v1/PostRegister', _getLoginData());
//               //!------------------------------------------------------------------------------------
//             },
//             child: const Text('Register'),
//           ),
//           const MediumVerticalPadding(),
//           // ElevatedButton(
//           //     onPressed: () async {
//           //       await base64Encode(); //! Convert assets to bit8 here
//           //       TestUIModel().post('/v1/UploadStaticFile', _getImageData());
//           //     },
//           //     child: const Text('GetImage')),
//           const MediumVerticalPadding(),
//           ElevatedButton(
//             //!----------------------[GET IMAGE FROM SEVER]------------------------------------------
//             onPressed: () async {
//               Future fileBase64 = _openFileExplorer();
//               // _getImageData(await fileBase64);
//               var imageDataString = TestUIModel().post(
//                   '/v1/UploadStaticFile', _getImageData(await fileBase64));
//               dynamic imageData = jsonDecode(await imageDataString);

//               setState(() {
//                 url = imageData['Data']['url'];
//                 print(url);
//               });
//             },
//             child: const Text('Add image +'),
//           ),
//           const MediumVerticalPadding(),
//           Image.network(
//             url,
//             width: 400,
//             height: 200,
//           ),
//         ],
//       ),
//     );
//   }
// }
// //

