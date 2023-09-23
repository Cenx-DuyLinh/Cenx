import 'dart:async';

void mainbuffer() {
  var object = myStream();
  object.takeWhile((event) => event > 7).listen(print);
  // object.listen(print, onError: print, onDone: () => print('done'));
}

Stream<int> myStream() async* {
  yield 15;
  yield 10;
  yield 5;
  throw 'Shit happened';
}

void main() async {
  var myStream = StreamController.broadcast();
  // myStream.stream.listen(print);

  myStream.stream.listen((event) {
    print('$event');
  });
  myStream.stream.listen((event) {
    print('$event 2');
  });
  myStream.sink.add('event');
  myStream.sink.add('event2');
  myStream.sink.add(2);

  myStream.close();
}
