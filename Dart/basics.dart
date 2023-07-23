
import 'dart:io'; // use this for when u wanna import stuff

void GettingStarted(){
  //var name = 'Linh';
  //Note: Can't use numbers for var name 
  //String value
  String name = "Linh2";

  //Interger
  int x = 31;

  //Constant and Final 
  const String fullname= "Duy Linh";
  final String nickname = "Tin";

  //declaring and not assigning -> return a null value
  var MyName;

  print(MyName);
}

void Variables(){
  //Data type
  //String 
  String firstname = "John";
  print('The name of the guy is $firstname');
  //Interger
  int mynum = 7;
  print('The 1st number is $mynum');
  //Doubles 
  double secondnum = 123.1412;
  print('The 2nd number is $secondnum');
  //Boolean 
  bool mybool = false;
  print('The bool is $mybool');
  
  //Dynamic
  dynamic fullname = "linh elder";
  print( 'dynamic $fullname');
}

void Lists(){
  //List 
  var mylist = [1,2,3];
  print(mylist);
  print(mylist[0]);

  //Change an item 
  mylist[0]= 69;
  print(mylist);

  var emptylist = [];
  print(emptylist);

  emptylist.add('hello');
  print(emptylist);

  emptylist.addAll([1,2,2]);
  print(emptylist);

  //Insert at specifics position (position, items)
  mylist.insert(3, 900);
  print(mylist);

  mylist.insertAll(1, [100,101,101,100]);
  print(mylist);

  //Remove list
  mylist.removeWhere((element) => element==100); //Remove all 100
  print(mylist);

  mylist.removeAt(2); // Remove at position 2
  print(mylist);

}

void Maps(){
  //Maps! Key/Value.pair 
  var topping = {'John':'Pepperonic', 'Mary':'Cheese'};
  print(topping);
  print(topping['John']);

  //Show values;
  print(topping.values);
  //Show keys:
  print(topping.keys);

  //Show lenght
  print(topping.length);

  //Add value 
  topping['Tim']='Sausage';
  print(topping);

  //Add many things
  topping.addAll({'Linh':'Soemthing', 'Ha':'Other things'});
  print(topping);

  //Remove stuff
  topping.remove('Linh');
  print(topping);

  topping.clear();
  print(topping);
}
void Loops(){
  //for loop
  var num = 5;
  for(var i = num;i>=1;i--){
    print(i);
  }
  //for in loop
  var names= ['john', 'tina', 'time'];
  for (var name in names){
    print(name);
  }
  //while loop
  while(num>=1){
    print(num);
    num--;
  }
}

void isstuff(){
  var num = 6;
  if (num == 5){
    print('hello');
  }

  else if(num == 3){
    print('wasssup');
  }
  else {
    print('fu');
  }
}

void function(){
  myFunc(String name,[name2]){ //The [] mean the var is optional
    return "Hello $name and $name2";
  }

  var thing = myFunc('john');
  print(thing);
}


void input(){
  //User input
  print('Enter your name');
  String? name = stdin.readLineSync();
  print('Hello $name');
}

void convertstuff(){
  //conver string, int, double 
  //string to int
  var a,b,c;
  a= 40;
  b = '1';
  c = a + int.parse(b);
  print('$a + $b = $c');

  //string double
  var a1,b1,c1;
  a1= 40;
  b1 = '0.01';
  c1 = a1 + double.parse(b1);
  print('$a1 + $b1 = $c1');

  //int to string
  var g,h,i;
  g = 40;
  i = '1';
  h = g.toString()+i;
  print('$g+$i=$h');
}

void inputconversion(){
  //User input type conversion
  print('Enter Number:');
  var num = stdin.readLineSync();
  var num2 = int.parse(num??'0') + 10; // ??'0': if null then = 0 
  print(num2 + 10);
}

void fizzbuzz(){
  int num = 1;
  while(num<=100){
    if(num % 5 == 0 && num %3 == 0){
      print('$num, FizzBuzz');
    }
    else if(num%3==0){
      print('$num, Fizz');
    }
    else if(num%5==0){
      print('$num, Buzz');
    }
    else print('$num');
    num++;
  }
}

void main(){
  var person1 = Person2();
  person1.name = 'john';
  person1.showData();
}
class Person{
  String? name, sex;
  int? age;

  //Constructor
  //Linh: basically the init phase
  Person(String name,sex, int age){
    this.name = name; 
    this.age = age ;
    this.sex = sex;
  }
  void showData(){
    print('Name: $name');
    print('Age: $age');
    print('Sex: $sex');
  }
}
class Person2{
  String? name, sex;
  int? age;

  //method
  //Linh: instead of init, u use function
  void addData(String name, sex, int age){
    this.name= name;
    this.sex = sex;
    this.age = age;
  }
  void showData(){
    print('Name: $name');
    print('Age: $age');
    print('Sex: $sex');
  }
}