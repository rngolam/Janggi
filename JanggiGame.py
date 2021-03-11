# Author: Richard Ngo-Lam
# Date: 3/3/2021
# Description: Simulates an abstract backend version of the Korean strategy board game, "Janggi".

class JanggiGame:
    """
    Represents a strategy board game where two players compete to checkmate each other's "General" board piece. The
    game has a 9 x 10 board, a set of board spaces, a game state, a dictionary of players, a dictionary to convert
    algebraic notation to standard coordinates, and a turn counter to
    keep track of the turn order.
    """
    pass
    # TODO

    def __init__(self):
        """
        Initializes a Janggi game with a 9 x 10 board, a set of board spaces, a game state, a list of Players, and
        a turn counter to keep track of the turn order.
        """

        self._board = GameBoard()
        self._board_x_length = 9
        self._board_y_length = 10
        self._players = {
            "blue": Player("blue"),
            "red":  Player("red")
        }
        self._game_state = "UNFINISHED"
        self._turn_counter = 0
        self._algebraic_notation = {}

        for player in self._players:
            for piece in self._players[player].get_pieces():
                starting_pos = piece.get_position()
                self._board.place_piece(starting_pos, piece)

        # Fill algebraic notation dictionary
        for ascii_val in range(ord('a'), ord('j')):
            self._algebraic_notation[chr(ascii_val)] = ascii_val - ord('a')
        for num in range(1, 11):
            self._algebraic_notation[str(num)] = num - 1

        self.print_board()

    def get_game_state(self):
        """
        Returns the game state.
        """
        return self._game_state

    def is_in_check(self, player):
        """
        Takes a player color as a parameter and returns True if their General board piece is in check and False if
        it is not.
        """
        player = self._players[player]
        return player.get_general().get_is_in_check()

    def make_move(self, string_1, string_2):
        """
        Takes a start and end position (strings in algebraic notation) and converts them to tuple coordinates. First
        checks whether a piece exists in the starting location. If not, returns False. Then checks the piece's Player
        color. If it does not correspond with the Player's current turn, returns False. Lastly, checks that pieces set
        of legal moves. If the end location is not in the set of legal moves, returns False. Additionally, checks
        whether the current move will either put the Player's own General in check (returns False) or the opposing
        Player's General in check. Finally, if all the above conditions are passed, returns True and updates the
        game board accordingly.
        """
        start_position = self.convert_algebraic_notation(string_1)
        end_position = self.convert_algebraic_notation(string_2)

        if self._game_state != "UNFINISHED":
            return False

        # if selected space is empty, return False
        if start_position not in self._board.get_occupied_spaces():
            return False

        player_piece = self._board.get_piece_at_coord(start_position)
        player = player_piece.get_player()
        opponent_piece = self._board.get_piece_at_coord(end_position)
        opponent = self._players[player.get_opponent_color()]

        if self._turn_counter % 2 == 0:
            turn = "blue"
        else:
            turn = "red"

        # if player selects a piece that is not theirs, return False
        if player.get_color() != turn:
            return False

        # player passes turn
        if start_position == end_position:
            self._turn_counter += 1
            self.print_board()
            return True

        # if player makes an illegal move, return False
        if end_position not in player_piece.get_move_range(self._board):
            return False

        # if player makes a move that puts their general in check, returns False

        # if player is in check and is still in check after the move is made, return False

        # check checkmate conditions

        # update game board and return True

        # Capture opponent piece
        if opponent_piece is not None:
            self._board.remove_piece(end_position)
            opponent.remove_piece(opponent_piece)
            opponent.remove_occupied_space(end_position)


        # Update board
        self._board.remove_piece(start_position)
        self._board.place_piece(end_position, player_piece)
        player_piece.set_position(end_position)
        player.remove_occupied_space(start_position)
        player.add_occupied_space(end_position)

        self._turn_counter += 1

        self.print_board()

        return True

    def convert_algebraic_notation(self, alg_not):
        """
        Takes a string in algebraic notation, converts it to a coordinate tuple, and returns the tuple.
        """
        x_coord = self._algebraic_notation[alg_not[0]]

        if len(alg_not) < 3:
            y_coord = self._algebraic_notation[alg_not[1]]

        else:
            y_coord = self._algebraic_notation[alg_not[1] + alg_not[2]]

        return (x_coord, y_coord)

    def print_board(self):
        """
        Prints the game board. For debugging purposes only.
        """
        self._board.print_board()


class Player:
    """
    Represents a player object. Has a color and a list of pieces as attributes.
    """
    pass
    # TODO

    def __init__(self, color):
        """
        Initializes a player with the parameterized color. Also creates a list of pieces with starting positions
        based on the player's color. Assigns the Player object to these pieces.
        """
        self._color = color
        self._opponent_color = None
        self._pieces = []
        self._occupied_spaces = set()
        if self._color == "blue":
            self._pieces.append(General((4, 8)))
            self._pieces.append(Guard((3, 9)))
            self._pieces.append(Guard((5, 9)))
            self._pieces.append(Horse((2, 9)))
            self._pieces.append(Horse((7, 9)))
            self._pieces.append(Elephant((1, 9)))
            self._pieces.append(Elephant((6, 9)))
            self._pieces.append(Chariot((0, 9)))
            self._pieces.append(Chariot((8, 9)))
            self._pieces.append(Cannon((1, 7)))
            self._pieces.append(Cannon((7, 7)))
            self._pieces.append(Soldier((0, 6)))
            self._pieces.append(Soldier((2, 6)))
            self._pieces.append(Soldier((4, 6)))
            self._pieces.append(Soldier((6, 6)))
            self._pieces.append(Soldier((8, 6)))

            self._opponent_color = "red"

        else:
            self._pieces.append(General((4, 1)))
            self._pieces.append(Guard((3, 0)))
            self._pieces.append(Guard((5, 0)))
            self._pieces.append(Horse((2, 0)))
            self._pieces.append(Horse((7, 0)))
            self._pieces.append(Elephant((1, 0)))
            self._pieces.append(Elephant((6, 0)))
            self._pieces.append(Chariot((0, 0)))
            self._pieces.append(Chariot((8, 0)))
            self._pieces.append(Cannon((1, 2)))
            self._pieces.append(Cannon((7, 2)))
            self._pieces.append(Soldier((0, 3)))
            self._pieces.append(Soldier((2, 3)))
            self._pieces.append(Soldier((4, 3)))
            self._pieces.append(Soldier((6, 3)))
            self._pieces.append(Soldier((8, 3)))

            self._opponent_color = "blue"

        for piece in self._pieces:
            piece.set_player(self)
            self._occupied_spaces.add(piece.get_position())

    def __repr__(self):
        return "Player(" + repr(self._color) + ")"

    def get_color(self):
        """

        """
        return self._color

    def get_opponent_color(self):
        """

        """
        return self._opponent_color

    def get_pieces(self):
        """

        """
        return self._pieces

    def remove_piece(self, piece):
        """

        """
        self._pieces.remove(piece)

    def get_general(self):
        """

        """
        return self._pieces[0]

    def add_occupied_space(self, coord):
        """

        """
        self._occupied_spaces.add(coord)

    def remove_occupied_space(self, coord):
        """

        """
        self._occupied_spaces.remove(coord)

    def get_occupied_spaces(self):
        """

        """
        return self._occupied_spaces


class GameBoard:
    """

    """
    def __init__(self):
        self._spaces = []
        self._x_length = 9
        self._y_length = 10
        self._all_spaces = set()
        self._available_spaces = set()
        self._palace_spaces = set()
        self._palace_diagonals = set()

        for column in range(self._x_length):
            self._spaces.append([])

            for row in range(self._y_length):
                coord = (column, row)
                self._spaces[column].append(Space(coord))
                self._all_spaces.add(coord)

        self._available_spaces = set(self._all_spaces)

        # Define palace spaces
        counter = 0
        for column in range(3, 6):
            for row in range(7, 10):
                coord = (column, row)
                self._palace_spaces.add(coord)
                if counter % 2 == 0:
                    self._palace_diagonals.add(coord)
                counter += 1
        counter = 0
        for column in range(3, 6):
            for row in range(0, 3):
                coord = (column, row)
                self._palace_spaces.add(coord)
                if counter % 2 == 0:
                    self._palace_diagonals.add(coord)
                counter += 1

        for coord in self._palace_spaces:
            x_coord, y_coord = coord
            self._spaces[x_coord][y_coord] = PalaceSpace(coord)


    def place_piece(self, coord, piece):
        """

        """
        x_coord, y_coord = coord
        space = self._spaces[x_coord][y_coord]
        space.place_piece(piece)
        self._available_spaces.remove(coord)

    def remove_piece(self, coord):
        """

        """
        x_coord, y_coord = coord
        space = self._spaces[x_coord][y_coord]
        space.remove_piece()
        self._available_spaces.add(coord)

    def get_all_spaces(self):
        """

        """
        return self._all_spaces

    def get_available_spaces(self):
        """

        """
        return self._available_spaces

    def get_occupied_spaces(self):
        """

        """
        return self._all_spaces - self._available_spaces    # set difference of spaces on the board and available spaces = occupied spaces

    def get_palace_spaces(self):
        """

        """
        return self._palace_spaces

    def get_palace_diagonals(self):
        """

        """
        return self._palace_diagonals

    def get_piece_at_coord(self, coord):
        """

        """
        x_coord, y_coord = coord
        space = self._spaces[x_coord][y_coord]
        return space.get_piece()

    def print_board(self):
        """
        Prints the game board. For debugging purposes.
        """

        print("  ", end=" ")

        for column in range(self._x_length):
            print(" " + chr(column + ord('a')) + " ", end=" ")

        print("")

        for row in range(self._y_length):

            if (row + 1) >= 10:
                print(row + 1, end=" ")
            else:
                print(row + 1, end="  ")

            for column in range(self._x_length):

                    print(self._spaces[column][row], end=" ")

            print("")


class Space:
    """

    """
    def __init__(self, coord):
        """
        """
        self._coord = coord
        self._piece = None
        self._is_occupied = False

    def __repr__(self):
        """

        """
        if self._piece is None:
            return "Square(" + repr(self._coord) + ", " + repr(self._piece) + ", " + repr(self._is_occupied) + ")"
        else:
            return self._piece

    def __str__(self):
        """

        """
        if self._piece is None:
            return " . "
        else:
            return str(self._piece)

    def place_piece(self, piece):
        """

        """
        self._piece = piece
        self._is_occupied = True

    def remove_piece(self):
        """

        """
        self._piece = None
        self._is_occupied = False

    def get_piece(self):
        """

        """
        return self._piece

    def get_coordinates(self):
        """

        """
        return self._coord

    def get_is_occupied(self):
        """

        """
        return self._is_occupied


class PalaceSpace(Space):
    """

    """

    def __repr__(self):
        """

        """
        if self._piece is None:
            return "PalaceSquare(" + repr(self._coord) + ", " + repr(self._piece) + ", " + repr(self._is_occupied) + ")"
        else:
            return self._piece

    def __str__(self):
        """

        """
        if self._piece is None:
            return " * "
        else:
            return str(self._piece)


class BoardPiece:
    """
    Represents a Piece on the game board. Has a Player object as an attribute, a tuple position, and a set of legal
    moves. Also has methods to get and set the piece's current position as well as get and set the piece's assigned
    Player.
    """
    pass
    # TODO

    def __init__(self, position):
        """

        """
        self._player = None
        self._color = None
        self._position = position
        self._move_range = set()

    def set_position(self, coord):
        """
        Sets the Board Piece's position.
        """
        self._position = coord

    def get_position(self):
        """
        Returns the Board Piece's location coordinates on the game board.
        """
        return self._position

    def set_player(self, player):
        """
        Sets the player that the piece belongs to.
        """
        self._player = player
        self._color = player.get_color()

    def get_player(self):
        """
        Returns the player that the piece belongs to.
        """
        return self._player


class General(BoardPiece):
    """
    Represents a General. Has methods to get the set of legal moves as well as to change positions. Also has methods to
    check whether the piece is in check or checkmate. Inherits from BoardPiece.
    """
    pass
    # TODO

    def __repr__(self):
        return self._color[0].upper() + "GN"

    def get_move_range(self, board):
        """

        """
        self._move_range.clear()

        palace_spaces = board.get_palace_spaces()
        palace_diagonals = board.get_palace_diagonals()
        allied_spaces = self._player.get_occupied_spaces()
        x_pos, y_pos = self._position

        if self._position in palace_diagonals:

            for x_coord in range(x_pos - 1, x_pos + 2):
                for y_coord in range(y_pos - 1, y_pos + 2):
                    if (x_coord, y_coord) in palace_spaces - allied_spaces:
                        self._move_range.add((x_coord, y_coord))

        # if not on a space connected by a diagonal line, can only move orthogonally
        else:

            for x_coord in range(x_pos - 1, x_pos + 2):
                if (x_coord, y_pos) in palace_spaces - allied_spaces:
                    self._move_range.add((x_coord, y_pos))

            for y_coord in range(y_pos - 1, y_pos + 2):
                if (x_pos, y_coord) in palace_spaces - allied_spaces:
                    self._move_range.add((x_pos, y_coord))

        return self._move_range

    def is_in_check(self):
        """

        """

    def is_in_checkmate(self):
        """
        """
        pass


class Guard(BoardPiece):
    """
    Has methods to get the set of legal moves as well as to change positions. Inherits from BoardPiece.
    """

    def __repr__(self):
        return self._color.upper()[0] + "GD"

    def get_move_range(self, board):
        """

        """
        self._move_range.clear()

        palace_spaces = board.get_palace_spaces()
        palace_diagonals = board.get_palace_diagonals()
        allied_spaces = self._player.get_occupied_spaces()
        x_pos, y_pos = self._position

        if self._position in palace_diagonals:

            for x_coord in range(x_pos - 1, x_pos + 2):
                for y_coord in range(y_pos - 1, y_pos + 2):
                    if (x_coord, y_coord) in palace_spaces - allied_spaces:
                        self._move_range.add((x_coord, y_coord))

        # if not on a space connected by a diagonal line, can only move orthogonally
        else:

            for x_coord in range(x_pos - 1, x_pos + 2):
                if (x_coord, y_pos) in palace_spaces - allied_spaces:
                    self._move_range.add((x_coord, y_pos))

            for y_coord in range(y_pos - 1, y_pos + 2):
                if (x_pos, y_coord) in palace_spaces - allied_spaces:
                    self._move_range.add((x_pos, y_coord))

        return self._move_range


class Horse(BoardPiece):
    """
    Has methods to get the set of legal moves as well as to change positions. Inherits from BoardPiece.
    """

    def __repr__(self):
        return self._color.upper()[0] + "HS"

    def get_move_range(self, board):
        """

        """
        self._move_range.clear()

        all_spaces = board.get_all_spaces()
        allied_spaces = self._player.get_occupied_spaces()
        x_pos, y_pos = self._position

        # check spaces horizontally
        for x_coord in range(x_pos - 1, x_pos + 2, 2):
            if (x_coord, y_pos) in all_spaces and board.get_piece_at_coord((x_coord, y_pos)) is None:
                for y_coord in range(y_pos - 1, y_pos + 2, 2):

                    x_offset = 0
                    if x_coord < x_pos:
                        x_offset -= 1
                    elif x_coord > x_pos:
                        x_offset += 1

                    if (x_coord + x_offset, y_coord) in all_spaces - allied_spaces:
                        self._move_range.add((x_coord + x_offset, y_coord))

        # check spaces vertically
        for y_coord in range(y_pos - 1, y_pos + 2, 2):
            if (x_pos, y_coord) in all_spaces and board.get_piece_at_coord((x_pos, y_coord)) is None:
                for x_coord in range(x_pos - 1, x_pos + 2, 2):

                    y_offset = 0
                    if y_coord < y_pos:
                        y_offset -= 1
                    elif y_coord > y_pos:
                        y_offset += 1

                    if (x_coord, y_coord + y_offset) in all_spaces - allied_spaces:
                        self._move_range.add((x_coord, y_coord + y_offset))

        return self._move_range


class Elephant(BoardPiece):
    """
    Has methods to get the set of legal moves as well as to change positions. Inherits from BoardPiece.
    """

    def __repr__(self):
        return self._color.upper()[0] + "EP"

    def get_move_range(self, board):
        """

        """
        self._move_range.clear()

        all_spaces = board.get_all_spaces()
        allied_spaces = self._player.get_occupied_spaces()
        x_pos, y_pos = self._position

        # check spaces horizontally
        for x_coord in range(x_pos - 1, x_pos + 2, 2):

            if (x_coord, y_pos) in all_spaces and board.get_piece_at_coord((x_coord, y_pos)) is None:
                for y_coord in range(y_pos - 1, y_pos + 2, 2):

                    x_offset = 0
                    if x_coord < x_pos:
                        x_offset -= 1

                    else:
                        x_offset += 1

                    if (x_coord + x_offset, y_coord) in all_spaces and board.get_piece_at_coord((x_coord + x_offset, y_coord)) is None:
                        for y_coord in range(y_pos - 2, y_pos + 3, 4):

                            x_offset = 0
                            if x_coord < x_pos:
                                x_offset -= 2

                            else:
                                x_offset += 2

                            if (x_coord + x_offset, y_coord) in all_spaces - allied_spaces:
                                self._move_range.add((x_coord + x_offset, y_coord))

        # check spaces vertically
        for y_coord in range(y_pos - 1, y_pos + 2, 2):
            if (x_pos, y_coord) in all_spaces and board.get_piece_at_coord((x_pos, y_coord)) is None:
                for x_coord in range(x_pos - 1, x_pos + 2, 2):

                    y_offset = 0
                    if y_coord < y_pos:
                        y_offset -= 1

                    else:
                        y_offset += 1

                    if (x_coord, y_coord + y_offset) in all_spaces and board.get_piece_at_coord((x_coord, y_coord + y_offset)) is None:
                        for x_coord in range(x_pos - 2, x_pos + 3, 4):

                            y_offset = 0
                            if y_coord < y_pos:
                                y_offset -= 2

                            else:
                                y_offset += 2

                            if (x_coord, y_coord + y_offset) in all_spaces - allied_spaces:
                                self._move_range.add((x_coord, y_coord + y_offset))

        return self._move_range


class Chariot(BoardPiece):
    """
    Has methods to get the set of legal moves as well as to change positions. Inherits from BoardPiece.
    """

    def __repr__(self):
        return self._color.upper()[0] + "CH"

    def get_move_range(self, board):
        """

        """
        self._move_range.clear()

        all_spaces = board.get_all_spaces()
        palace_diagonals = board.get_palace_diagonals()
        allied_spaces = self._player.get_occupied_spaces()
        x_pos, y_pos = self._position


        # check left
        x_offset = -1
        while (x_pos + x_offset, y_pos) in all_spaces:
            piece = board.get_piece_at_coord((x_pos + x_offset, y_pos))
            if piece is not None:
                if (x_pos + x_offset, y_pos) not in allied_spaces:
                    self._move_range.add((x_pos + x_offset, y_pos))
                break
            self._move_range.add((x_pos + x_offset, y_pos))
            x_offset -= 1

        # check right
        x_offset = 1
        while (x_pos + x_offset, y_pos) in all_spaces:
            piece = board.get_piece_at_coord((x_pos + x_offset, y_pos))
            if piece is not None:
                if (x_pos + x_offset, y_pos) not in allied_spaces:
                    self._move_range.add((x_pos + x_offset, y_pos))
                break
            self._move_range.add((x_pos + x_offset, y_pos))
            x_offset += 1

        # check up
        y_offset = -1
        while (x_pos, y_pos + y_offset) in all_spaces:
            piece = board.get_piece_at_coord((x_pos, y_pos + y_offset))
            if piece is not None:
                if (x_pos, y_pos + y_offset) not in allied_spaces:
                    self._move_range.add((x_pos, y_pos + y_offset))
                break
            self._move_range.add((x_pos, y_pos + y_offset))
            y_offset -= 1

        # check down
        y_offset = 1
        while (x_pos, y_pos + y_offset) in all_spaces:
            piece = board.get_piece_at_coord((x_pos, y_pos + y_offset))
            if piece is not None:
                if (x_pos, y_pos + y_offset) not in allied_spaces:
                    self._move_range.add((x_pos, y_pos + y_offset))
                break
            self._move_range.add((x_pos, y_pos + y_offset))
            y_offset += 1

        # check diagonal movement within palaces
        if self._position in palace_diagonals:

            # Piece is in center of palace
            if x_pos == 4:  # piece is in palace center
                for x_coord in range(x_pos - 1, x_pos + 2):
                    for y_coord in range(y_pos - 1, y_pos + 2):
                        if abs(x_coord - x_pos) == abs(y_coord - y_pos):

                            piece = board.get_piece_at_coord((x_coord, y_coord))

                            if piece is None or (x_coord, y_coord) not in allied_spaces:
                                self._move_range.add((x_coord, y_coord))

            # Piece is in corner of palace
            else:
                palace_center = None

                # Find palace center relative to position
                for x_coord in range(x_pos - 1, x_pos + 2):
                    for y_coord in range(y_pos - 1, y_pos + 2):

                        # palace center found
                        if abs(x_coord - x_pos) == abs(y_coord - y_pos) and (x_coord, y_coord) in palace_diagonals and \
                                (x_coord, y_coord) != self._position:

                            palace_center = (x_coord, y_coord)
                            break

                if palace_center[0] < x_pos:
                    x_offset = -1
                else:
                    x_offset = 1

                if palace_center[1] < y_pos:
                    y_offset = -1
                else:
                    y_offset = 1

                while (x_pos + x_offset, y_pos + y_offset) in palace_diagonals:

                    piece = board.get_piece_at_coord((x_pos + x_offset, y_pos + y_offset))

                    if piece is not None:
                        if (x_pos + x_offset, y_pos + y_offset) not in allied_spaces:
                            self._move_range.add((x_pos + x_offset, y_pos + y_offset))
                        break
                    self._move_range.add((x_pos + x_offset, y_pos + y_offset))
                    x_offset += x_offset
                    y_offset += y_offset

        return self._move_range

class Cannon(BoardPiece):
    """
    Has methods to get the set of legal moves as well as to change positions. Inherits from BoardPiece.
    """

    def __repr__(self):
        return self._color.upper()[0] + "CN"

    def get_move_range(self, board):
        """

        """
        self._move_range.clear()

        all_spaces = board.get_all_spaces()
        palace_diagonals = board.get_palace_diagonals()
        allied_spaces = self._player.get_occupied_spaces()
        x_pos, y_pos = self._position

        # check left
        x_offset = -1
        pieces_between = 0
        while (x_pos + x_offset, y_pos) in all_spaces:

            piece = board.get_piece_at_coord((x_pos + x_offset, y_pos))

            if piece is not None:
                if pieces_between == 1 or isinstance(piece, Cannon):
                    if ((x_pos + x_offset, y_pos)) not in allied_spaces and isinstance(piece, Cannon) is False:
                        self._move_range.add((x_pos + x_offset, y_pos))
                    break
                pieces_between += 1

            else:
                if pieces_between == 1:
                    self._move_range.add((x_pos + x_offset, y_pos))
            x_offset -= 1

        # check right
        x_offset = 1
        pieces_between = 0
        while (x_pos + x_offset, y_pos) in all_spaces:

            piece = board.get_piece_at_coord((x_pos + x_offset, y_pos))

            if piece is not None:
                if pieces_between == 1 or isinstance(piece, Cannon):
                    if ((x_pos + x_offset, y_pos)) not in allied_spaces and isinstance(piece, Cannon) is False:
                        self._move_range.add((x_pos + x_offset, y_pos))
                    break
                pieces_between += 1

            else:
                if pieces_between == 1:
                    self._move_range.add((x_pos + x_offset, y_pos))
            x_offset += 1

        # check up
        y_offset = -1
        pieces_between = 0
        while (x_pos, y_pos + y_offset) in all_spaces:

            piece = board.get_piece_at_coord((x_pos, y_pos + y_offset))

            if piece is not None:
                if pieces_between == 1 or isinstance(piece, Cannon):
                    if ((x_pos, y_pos + y_offset)) not in allied_spaces and isinstance(piece, Cannon) is False:
                        self._move_range.add((x_pos, y_pos + y_offset))
                    break
                pieces_between += 1

            else:
                if pieces_between == 1:
                    self._move_range.add((x_pos, y_pos + y_offset))
            y_offset -= 1

        # check down
        y_offset = 1
        pieces_between = 0
        while (x_pos, y_pos + y_offset) in all_spaces:

            piece = board.get_piece_at_coord((x_pos, y_pos + y_offset))

            if piece is not None:
                if pieces_between == 1 or isinstance(piece, Cannon):
                    if ((x_pos, y_pos + y_offset)) not in allied_spaces and isinstance(piece, Cannon) is False:
                        self._move_range.add((x_pos, y_pos + y_offset))
                    break
                pieces_between += 1

            else:
                if pieces_between == 1:
                    self._move_range.add((x_pos, y_pos + y_offset))
            y_offset += 1

        # check diagonal movement within palaces
        # diagonal movement is only permitted if center of palace is occupied
        if self._position in palace_diagonals:

            palace_center = None

            # Find palace center relative to position
            for x_coord in range(x_pos - 1, x_pos + 2):
                for y_coord in range(y_pos - 1, y_pos + 2):

                    # palace center found
                    if abs(x_coord - x_pos) == abs(y_coord - y_pos) and (x_coord, y_coord) in palace_diagonals and \
                            (x_coord, y_coord) != self._position:
                        palace_center = (x_coord, y_coord)
                        break

            piece_at_center = board.get_piece_at_coord(palace_center)

            # Cannon can only jump diagonally within palace if center space is occupied by a non-Cannon piece
            if piece_at_center is not None and isinstance(piece_at_center, Cannon) is False:

                if palace_center[0] < x_pos:
                    x_offset = -2
                else:
                    x_offset = 2

                if palace_center[1] < y_pos:
                    y_offset = -2
                else:
                    y_offset = 2

                piece_at_destination = board.get_piece_at_coord((x_pos + x_offset, y_pos + y_offset))

                if piece_at_destination is None or (piece_at_destination is not None and (x_pos + x_offset, y_pos + y_offset) not in allied_spaces):
                    self._move_range.add((x_pos + x_offset, y_pos + y_offset))

        return self._move_range


class Soldier(BoardPiece):
    """
    Has methods to get the set of legal moves as well as to change positions. Inherits from BoardPiece.
    """

    def __repr__(self):
        return self._color.upper()[0] + "SD"

    def get_move_range(self, board):
        """

        """
        self._move_range.clear()

        all_spaces = board.get_all_spaces()
        palace_diagonals = board.get_palace_diagonals()
        allied_spaces = self._player.get_occupied_spaces()
        x_pos, y_pos = self._position

        y_offset = None

        if self._color == "blue":
            y_offset = -1

        elif self._color == "red":
            y_offset = 1

        for x_coord in range(x_pos - 1, x_pos + 2):
            if (x_coord, y_pos) in all_spaces - allied_spaces:
                self._move_range.add((x_coord, y_pos))

        if (x_pos, y_pos + y_offset) in all_spaces - allied_spaces:
            self._move_range.add((x_pos, y_pos + y_offset))

        # Diagonal movement augmentation in palace
        if self._position in palace_diagonals:
            for x_coord in range(x_pos - 1, x_pos + 2):
                if (x_coord, y_pos + y_offset) in palace_diagonals - allied_spaces:
                    self._move_range.add((x_coord, y_pos + y_offset))

        return self._move_range
