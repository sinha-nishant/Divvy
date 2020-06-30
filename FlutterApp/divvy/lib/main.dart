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
      theme: ThemeData.dark(),
      home: MyHomePage(title: 'Divvy'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, this.title}) : super(key: key);
  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  Future<void> _payWithVenmo(double amount) async {
    String url =
        'venmo://paycharge?txn=pay&recipients=ArjunMitra&amount=$amount&note=Divvy';
    if (await canLaunch(url)) {
      await launch(url);
    } else {
      throw 'Could not launch $url';
    }
  }

  @override
  Widget build(BuildContext context) {
    double balance = 130.95;
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body: ListView(
        padding: new EdgeInsets.all(20),
        children: <Widget>[
          Column(
            children: <Widget>[
              AspectRatio(
                  aspectRatio: 2,
                  child: Container(
                      color: Colors.blue,
                      child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: <Widget>[
                            Text('Balance', style: TextStyle(fontSize: 30)),
                            Padding(padding: new EdgeInsets.all(5)),
                            Text('\$$balance', style: TextStyle(fontSize: 80)),
                            Padding(padding: new EdgeInsets.all(20))
                          ]))),
              Container(
                  width: MediaQuery.of(context).size.width,
                  child: RaisedButton(
                    onPressed: () => setState(() {
                      Future<void> _launched = _payWithVenmo(balance);
                    }),
                    child: const Text('Pay with Venmo',
                        style: TextStyle(fontSize: 20.0)),
                  ))
            ],
          ),
        ],
      ),
    );
  }
}
