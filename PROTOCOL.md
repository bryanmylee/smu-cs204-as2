# Reverse Engineering Connect 4

## Deconstructing messages

### Packet breakdown

1 -- 16: client logging in.

47 -- 50: client starting a new game.

57 -- 64: client made a move (3), server responded (7).

71 -- 78: client made a move (1), server responded (1).

91 -- 92: client left the game.

93 -- 98: client A logging in.

105 -- 110: client B logging in.

136 -- 139: client A starting a new game.

140 -- 143: client B starting a new game.

150 -- 151: client B left the game.

152 -- 153: client A left the game.

160 -- 165: client logging in.

166 -- 169: client starting a new game.

182 -- 189: client made a move (1), server made a move (5).

196 -- 203: client made a move (1), server made a move (1).

210 -- 217: client made a move (1), server made a move (1).

218 -- 225: client made a move (7), server made a move (6).

238 -- 245: client made a move (7), server made a move (7).

246 -- 253: client made a move (6), server made a move (7).

...

300 -- 305: client made an invalid move (1)

338 -- 343: client loses.

380 -- 387: client starts a new game again.

388 -- 389: client leaves the game.

#### Logging In

```
s to c: 2734 // What type of game?
```

#### Start New Game

```
c to s: 374b // Start a new game of type 4b
s to c: 1a34 // Confirm new game
```

#### Client Makes a Move 3, Server Responds 7

```
c to s: 3f02 // Make move at index 2
s to c: 3c02 // Confirm move at index 2
s to c: 5506 // Respond with index 6
s to c: 1a34 // NOOP
```

#### Client Makes a Move 1, Server Responds 1

```
c to s: 3f00 // Make move at index 0
s to c: 3c00 // Confirm move at index 0
s to c: 5500 // Respond with index 0
s to c: 1a34 // NOOP
```

#### Client Loses

```
c to c: 3f01 // Make move at index 1
s to c: 3c01 // Confirm move at index 1
s to c: 5502 // Respond with index 2
s to c: 0b18 // Server wins
```

#### Client Wins

```
c to s: 3f02 // Make move at index 2
s to c: 3c02 // Confirm move at index 2
s to c: 0b3d // Client wins
```

#### Tie

```
c to s: 3f00 // Make move at index 0
s to c: 3c00 // Confirm move at index 0
s to c: 5506 // Respond with index 6
s to c: 0b35 // It's a tie
```

#### Play Again

```
c to s: 2234 // Play again
s to c: 2734 // What type of game?
c to s: 374b // Start a new game of type 4b
s to c: 1a34 // Confirm new game
```

#### Don't Play Again

```
c to s: 2a34 // Don't play again
s to c: FIN
```

#### Forfeit

```
c to s: 4134
s to c: 0b18
```



#### Quit

```
c to s: FIN
```

#### Invalid Move

```
c to s: 3f00 // Make move at index 0
s to c: 2300 // Deny index 0
s to c: 1a34 // NOOP
```

```
c to s: 3f02 // Make move at index 2
s to c: 2302 // Deny index 2
s to c: 1a34 // NOOP
```























