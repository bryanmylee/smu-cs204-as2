# CS204 Networking Assignment 2

We were tasked to determine the codes used in the protocol for the game. The commands found are stored in `commands.txt`.

As an extra challenge, we were tasked with building our own server implementation to play Connect 4.

`server.py` contains my implementation of the server, however does not include any AI to determine the next best move. Instead, it simply picks a random move.

`sample/` contains the server and client to be run and analysed.
* `server.jar` and `client.jar` work out-of-the-box.
* `dummy_client.jar` reads the `commands.txt` file to determine what command to use. It is meant to help us debug our answers.

## Running the server

To run the server, simply run:

```bash
$ python3 server.py [{server port}]
```

