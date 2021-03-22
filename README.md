# Janggi

**Janggi** is a Korean strategy board game that is derived from and bears similarities to xiangqi (Chinese chess). This program allows users to play an abstract backend version of Janggi in a Python console.

The rules of Janggi can be read [here](https://en.wikipedia.org/wiki/Janggi). Note that this version of the game begins with the positions of the Elephant and Horse pieces transposed on the right side. The game also does not end in a draw if the two player's General pieces face each other from across the board.

**Instructions**

* Begin a new game by instantiating a new game object (e.g. `game = JanggiGame()`).
* The Blue player moves first. Moves are made by calling `make_move` on the game with two string parameters in algebraic notation, with columns labeled a-i and rows labeled 1-10, with row 1 being the Red side and row 10 the Blue side (e.g. `game.make_move('a7','b7')`)
  * `make_move` will return `False` if a move is attempted on a finished game, if a board piece is not selected, if a player attempts to move when it is not their turn, if an invalid move is made, if a player makes a move that places their own General in check, or if a player fails to counter a check. Otherwise, the game board will be updated and this method will return `True`.
  * Unlike chess, players can choose to pass their turn in Janggi. This is performed by selecting a coordinate currently occupied by one of their pieces and passing it as both a start and end location to `make_move` (e.g. `game.make_move('a1,a1')`).
* To verify whether a player's General is in check, call `is_in_check` with the parameterized player color as a string (e.g. `game.is_in_check('blue')`).
* To check the current game state, call `get_game_state`, which will return `'UNFINISHED'`, `'BLUE_WON'`, or '`RED_WON'`.
* The game ends when one player places their opponent's General in checkmate, leaving the opponent with no valid moves to counter the check.

**Abbreviations**
* GN = General
* GD = Guard
* HS = Horse
* EP = Elephant
* CH = Chariot
* CN = Cannon
* SD = Soldier

**Example Usage**
```
game = JanggiGame()
move_result = game.make_move('c1', 'e3') # should return False because it's not Red's turn
move_result = game.make_move('a7,'b7') # should return True
blue_in_check = game.is_in_check('blue') # should return False
game.make_move('a4', 'a5') # should return True
state = game.get_game_state() # should return UNFINISHED
game.make_move('b7','b6') # should return True
game.make_move('b3','b6') # should return False because it's an invalid move
game.make_move('a1','a4') # should return True
game.make_move('c7','d7') # should return True
game.make_move('a4','a4') # this will pass the Red player's turn and return True
```

**Initial Board Setup**

![image](https://user-images.githubusercontent.com/69094063/111979348-f7cb6780-8ad2-11eb-95f9-86c099d93414.png)

**Example Game Played Out**
```
game = JanggiGame()
game.make_move('e7', 'e6')
game.make_move('e2', 'e2')
game.make_move('e6', 'e5')
game.make_move('e2', 'e2')
game.make_move('e5', 'e4')
game.make_move('e2', 'e2')
game.make_move('e4', 'd4')
game.make_move('e2', 'e2')
game.make_move('d4', 'c4')
game.make_move('e2', 'e2')
game.make_move('a10', 'a9')
game.make_move('e2', 'e2')
game.make_move('a9', 'd9')
game.make_move('e2', 'e2')
game.make_move('d9', 'd8')
game.make_move('i1', 'i2')
game.make_move('e9', 'e9')
game.make_move('i2', 'g2')
game.make_move('e9', 'e9')
game.make_move('i4', 'h4')
game.make_move('e9', 'e9')
game.make_move('h3', 'h5')
game.make_move('i10', 'i9')
game.make_move('e2', 'e2')
game.make_move('i9', 'g9')
game.make_move('e2', 'e2')
game.make_move('g9', 'g8')
game.make_move('e2', 'e2')
game.make_move('h8', 'f8')
game.make_move('f1', 'e1')
game.make_move('g7', 'f7')
game.make_move('g4', 'f4')
game.make_move('e9', 'e9')
game.make_move('f4', 'e4')

# Check
game.make_move('b8', 'e8')
game.make_move('e4', 'f4')
game.make_move('e9', 'e9')
game.make_move('f4', 'g4')
game.make_move('c7', 'd7')
game.make_move('e2', 'e2')

# Checkmate
game.make_move('d7', 'e7')
```
![image](https://user-images.githubusercontent.com/69094063/111979525-2cd7ba00-8ad3-11eb-8cba-565351fcfe73.png)

As seen above, the Red player's General is currently threatened by one of the Blue player's Cannons. The Blue player's two Cannons at e8 and f8, as well as their Chariot at d8, are capable of attacking every available square in the Red player's palace. Because the Red player is incapable of moving their General to safety, blocking these attack paths, or capturing Blue's pieces in question, the game is over.
