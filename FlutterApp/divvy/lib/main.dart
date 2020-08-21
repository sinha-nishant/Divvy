import 'dart:async';
import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Divvy',
      theme: ThemeData(
          brightness: Brightness.dark,
          primaryColor: Colors.black,
          primarySwatch: Colors.blue,
          backgroundColor: Colors.black),
      home: MyHomePage(title: 'Divvy'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  final String title;
  MyHomePage({Key key, this.title}) : super(key: key);

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

Future<void> _payWithVenmo() async {
  double balance = 130.95;
  String url =
      'venmo://paycharge?txn=pay&recipients=ArjunMitra&amount=$balance&note=Divvy';
  if (await canLaunch(url)) {
    await launch(url);
  } else {
    throw 'Could not launch $url';
  }
}

ListTile someTile = ListTile(
    leading: Text('MAY\n25',
        textAlign: TextAlign.center, style: TextStyle(color: Colors.black)),
    title: Text(
      '23rd Street Cafe',
      textAlign: TextAlign.center,
      style: TextStyle(color: Colors.black),
    ),
    trailing: Text(
      '\$13',
      style: TextStyle(fontSize: 15, color: Colors.black),
    )
    // subtitle: Text('Subtitle'),
    );

class RecentOrders {
  static Container of(BuildContext context, double balance) {
    return Container(
        decoration: BoxDecoration(
            color: Theme.of(context).accentColor,
            borderRadius: BorderRadius.circular(20)),
        width: MediaQuery.of(context).size.width * 0.9,
        height: MediaQuery.of(context).size.height * 0.5,
        child: ListView(padding: EdgeInsets.all(20), children: <Widget>[
          someTile,
          someTile,
          someTile,
          someTile,
          someTile,
          someTile,
          someTile,
          someTile,
          someTile
        ]));
  }
}

class BalanceDisplay {
  static Container of(BuildContext context, double balance) {
    return Container(
        width: MediaQuery.of(context).size.width * 0.9,
        height: MediaQuery.of(context).size.height * 0.2,
        child: Card(
            color: Theme.of(context).accentColor,
            shape: ContinuousRectangleBorder(
                borderRadius: BorderRadius.circular(35)),
            child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  Text('Balance',
                      style: TextStyle(fontSize: 25, color: Colors.black)),
                  Text('\$$balance',
                      style: TextStyle(fontSize: 75, color: Colors.black)),
                ])));
  }
}

Container sendButton = Container(
    width: 80,
    height: 80,
    child: FloatingActionButton(
      onPressed: () => _payWithVenmo(),
      child: Icon(
        Icons.attach_money,
        size: 50,
      ),
    ));

class _MyHomePageState extends State<MyHomePage> {
  @override
  Widget build(BuildContext context) {
    double balance = 130.95;
    return Scaffold(
      backgroundColor: Theme.of(context).backgroundColor,
      appBar: AppBar(
        title: Text(widget.title),
      ),
      floatingActionButton: sendButton,
      body: ListView(
        padding: EdgeInsets.all(20),
        physics: NeverScrollableScrollPhysics(),
        children: <Widget>[
          Column(
            children: <Widget>[BalanceDisplay.of(context, balance)],
          ),
          Padding(padding: EdgeInsets.all(10)),
          RecentOrders.of(context, balance)
        ],
      ),
    );
  }
}
