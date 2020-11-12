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

    def is_full(self):
        if self.mask == 279258638311359:
            return True
        return False

    def print_board(self):
        mask = self.mask
        pieces = self.pieces
        for i in range(49):
            m = mask % 2
            p = pieces % 2
            if i % 7 == 6:
                print()
            elif m == 0:
                print("0", end="")
            elif m == 1 and p == 0:
                print("c", end="")
            elif m == 1 and p == 1:
                print("s", end="")
            mask //= 2
            pieces //= 2


game = Game()
game.make_move(False, 0)
game.make_move(True, 0)
game.make_move(False, 0)
game.make_move(True, 1)
game.make_move(False, 0)
game.make_move(True, 0)
game.make_move(False, 0)
game.print_board()
print(game.win(True))
print(game.win(False))
