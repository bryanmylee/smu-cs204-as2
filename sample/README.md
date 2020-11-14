# Sample client and servers

To run the server, use Java and specify its port.

```bash
$ java -jar server.jar 1500
```

To run the client, specify the server host and port.

```bash
$ java -jar client.jar localhost 1500
```

To run the dummy client, specify the server host, port, and the location of the `commands.txt` file.

```bash
$ java -jar dummy_client.jar localhost 1500 ../commands.txt
```

