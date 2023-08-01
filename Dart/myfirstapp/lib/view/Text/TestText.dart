// ignore_for_file: file_names

import 'package:flutter/material.dart';

class TestText extends StatelessWidget {
  final String input;
  const TestText({required this.input, Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return RichText(
      text: TextSpan(
        text: input,
        style: const TextStyle(fontWeight: FontWeight.bold,color: Colors.amber)

      )
    );
  }
}