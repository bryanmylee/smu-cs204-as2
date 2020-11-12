from datetime import datetime
import random
import selectors
import socket
import sys


class Game:
    # Define the game board with bitstrings.
    # https://github.com/denkspuren/BitboardC4/blob/master/BitboardDesign.md
    def __init__(self):
        self.mask = 0
        # The server's pieces for this game.
        self.pieces = 0

    @property
    def client_pieces(self):
        return self.mask ^ self.pieces

    def win(self, is_server):
        if is_server:
            return self.connected_four(self.pieces)
        return self.connected_four(self.client_pieces)

    def connected_four(self, pieces):
        # Check horizontal.
        m = pieces & (pieces >> 7)
        if m & (m >> 14):
            return True
        # Check primary diagonal.
        m = pieces & (pieces >> 6)
        if m & (m >> 12):
            return True
        # Check secondary diagonal.
        m = pieces & (pieces >> 8)
        if m & (m >> 16):
            return True
        # Check vertical.
        m = pieces & (pieces >> 1)
        if m & (m >> 2):
            return True
        return False

    def is_full(self):
        return self.mask == 279258638311359

    def make_move(self, is_server, col):
        new_piece = 1 << (col * 7)
        # Check if column is already full.
        if self.mask & new_piece << 5:
            return False
        # Add a piece to the board.
        old_mask = self.mask
        self.mask = self.mask | (self.mask + new_piece)
        if is_server:
            # Update the server's pieces.
            self.pieces = self.pieces | (self.mask ^ old_mask)
        return True


class Client:
    def __init__(self, conn):
        self.conn = conn
        self.game = Game()


def get_timestamp(now=None):
    if now is None:
        now = datetime.now()
    return now.strftime("%H:%M:%S")


def get_host_port():
    host = "127.0.0.1"
    port = 1500
    if len(sys.argv) >= 2:
        port = int(sys.argv[1])
    return host, port


def create_async_server_socket(host, port):
    # Create an INET, STREAM (TCP) socket.
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    server.setblocking(False)
    print(f"{get_timestamp()} Server waiting for Clients on port {port}.")
    return server


def accept_fn(server, mask, clients):
    global sel
    print("NEW PLAYER JOINED THE SERVER")
    conn, addr = server.accept()
    conn.setblocking(False)
    host, port = addr
    client = Client(conn)
    clients[conn.fileno()] = client
    init_game(client)
    sel.register(conn, selectors.EVENT_READ, listen_fn)


def listen_fn(conn, mask, clients):
    global sel
    print("RECEIVED A MESSAGE")
    # Get the matching Client object for the given connection.
    client = clients[conn.fileno()]
    # Non-blocking conn should be ready for just one recv.
    data_bytes = client.conn.recv(1024)
    if not data_bytes:
        logout(client, clients, proper=False)
    elif data_bytes[0] == 0x37:
        start_game(client, data_bytes[1])
    elif data_bytes[0] == 0x3f:
        make_move(client, data_bytes[1])
    elif data_bytes[0] == 0x41:
        forfeit(client)
    elif data_bytes[0] == 0x22:
        # Play again.
        init_game(client)
    elif data_bytes[0] == 0x2a:
        # Don't play again.
        logout(client, clients)


def init_game(client: Client):
    global port
    print("INIT NEW GAME")
    client.conn.send(bytes([0x27, 0x34]))


def logout(asker: Client, clients, proper=True):
    global sel
    print("PLAYER ENDING GAME AND LOGGING OUT")
    try:
        asker.conn.close()
    except:
        pass
    clients.pop(asker.conn.fileno(), None)
    sel.unregister(asker.conn)


def start_game(client: Client, game_type):
    print(f"GAME TYPE {game_type}")
    client.game = Game()
    client.conn.send(bytes([0x1a, 0x34]))


def make_move(client: Client, move):
    print(f"PLAYER MADE MOVE {move}")
    valid = client.game.make_move(is_server=False, col=move)
    # Invalid move.
    if not valid:
        client.conn.send(bytes([0x23, move]))
        client.conn.send(bytes([0x1a, 0x34]))
        return
    # Confirm move.
    client.conn.send(bytes([0x3c, move]))
    # Reply if client wins.
    if client.game.win(is_server=False):
        client.conn.send(bytes([0x0b, 0x3d]))
        return
    s_move = random.randint(0, 6)
    while not client.game.make_move(is_server=True, col=s_move):
        s_move += 1
        s_move %= 7
    print(f"SERVER MADE MOVE {s_move}")
    # Reply with server move.
    client.conn.send(bytes([0x55, s_move]))
    # Check if server won.
    if client.game.win(is_server=True):
        client.conn.send(bytes([0x0b, 0x18]))
        return
    # Check if tie.
    if client.game.is_full():
        client.conn.send(bytes([0x0b, 0x35]))
        return
    client.conn.send(bytes([0x1a, 0x34]))


def forfeit(client: Client):
    client.conn.send(bytes([0x0b, 0x18]))


if __name__ == "__main__":
    global port
    global sel
    host, port = get_host_port()
    server = create_async_server_socket(host, port)
    # Create a selector with socket object key and a function value that
    # accepts a socket, mutex mask, and a map from socket file number to socket.
    sel = selectors.DefaultSelector()
    sel.register(server, selectors.EVENT_READ, accept_fn)

    # A map from a socket file number key to a Client object.
    clients = {}
    while True:
        # Get all socket object keys in the selector.
        for key, mask in sel.select():
            # Either the accept_fn or listen_fn.
            fn = key.data
            conn = key.fileobj
            fn(conn, mask, clients)



