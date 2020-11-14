# Sample client and servers

To run the server, use Java and specify its port.

```
java -jar server.jar 1500
```

To run the client, specify the server host and port.

```
java -jar client.jar localhost 1500
```

To run the dummy client, specify the server host, port, and the location of the `commands.txt` file.

```
java -jar dummy_client.jar localhost 1500 ../commands.txt
```

