# Author: Richard Ngo-Lam
# Date: 3/11/2021
# Description: Simulates an abstract backend version of the Korean strategy board game, "Janggi".

import copy


class JanggiGame:
    """
    Represents a strategy board game where two players compete to checkmate each other's "General" board piece. The
    game has a 9 x 10 GameBoard, a set of board Spaces, a game state, a dictionary of players, a dictionary to convert
    algebraic notation to standard coordinates, and a turn counter to keep track of the turn order. Has methods to
    get the current game state, get whether a certain Player is in check, make a move, update the GameBoard, verify
    whether a move leaves a Player in check, verify checkmate, convert algebraic notation to tuple coordinates, get the
    GameBoard, get the Player dictionary, and print the GameBoard.
    """

    def __init__(self):
        """
        Initializes a Janggi game with a 9 x 10 GameBoard, a dictionary of Players, a set of board spaces, a game state,
        a game state, a turn counter, and a dictionary of algebraic notation inputs with their corresponding
        coordinates.
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

        # Place player pieces on board
        for player in self._players:
            for piece in self._players[player].get_pieces():
                starting_pos = piece.get_position()
                self._board.place_piece(starting_pos, piece)

        # Fill algebraic notation dictionary
        for ascii_val in range(ord('a'), ord('j')):
            self._algebraic_notation[chr(ascii_val)] = ascii_val - ord('a')
        for num in range(1, 11):
            self._algebraic_notation[str(num)] = num - 1

        # self.print_board()

    def __repr__(self):
        return "JanggiGame(" + repr(self._game_state) + ", " + repr(self._turn_counter) + ")"

    def get_game_state(self):
        """
        Returns the game state.
        """
        return self._game_state

    def is_in_check(self, player):
        """
        Takes a Player color as a parameter and returns True if that Player is in check and False if they are not.
        """
        player = self._players[player]
        return player.get_is_in_check()

    def make_move(self, string_1, string_2):
        """
        Takes a start and end position (strings in algebraic notation) and converts them to tuple coordinates. Returns
        False if a move is attempted after the game is already finished, if a selected space is empty, if a Player acts
        out of turn, if a Player passes their turn while in check, if a Player passes their turn while in check, if a
        move is outside of a Piece's range, or if a Player makes a move that leaves them in check. Otherwise, updates
        the GameBoard and tests whether the move leaves the Player's opponent in check (and if so, verifies checkmate
        conditions to determine a winner) and returns True.
        """

        start_position = self.convert_algebraic_notation(string_1)
        end_position = self.convert_algebraic_notation(string_2)

        # Player attempts move during finished game
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

        # if Player acts out of turn
        if player.get_color() != turn:
            return False

        # Player passes turn
        if start_position == end_position:

            if player.get_is_in_check() is True:    # Player cannot pass turn while in check
                return False

            else:
                self._turn_counter += 1
                # self.print_board()
                return True

        # Player attempts to move outside of a Piece's range
        if end_position not in player_piece.get_move_range(self._board):
            return False

        # Player makes a move that leaves themselves in check, returns False
        # Copy the current game state and simulate whether the move leaves Player in check
        test_game = copy.deepcopy(self)
        if self.move_leaves_player_in_check(test_game, start_position, end_position):
            return False

        # At this point, all criteria for a legal move have been satisfied

        # Update the game board
        self.update_board(self._board, player, opponent, player_piece, opponent_piece, start_position, end_position)

        # Player made a legal move that counters any check
        if player.get_is_in_check() is True:
            player.set_is_in_check(False)

        # If the opponent's General is in the Player's list of attacked spaces, they are in check
        if opponent.get_general().get_position() in player.get_threat_range(self._board):
            opponent.set_is_in_check(True)

            # Test whether this move results in a checkmate
            if self.verify_checkmate(opponent) is True:
                self._game_state = player.get_color().upper() + "_WON"

        self._turn_counter += 1

        # self.print_board()

        return True

    def update_board(self, board, player, opponent, player_piece, opponent_piece, start_position, end_position):
        """
        Updates the actual (or simulated) GameBoard by removing any captured pieces (if applicable) and updating the
        position of the moving Piece.
        """

        # Capture opponent Piece
        if opponent_piece is not None:
            board.remove_piece(end_position)
            opponent.remove_piece(opponent_piece)
            opponent.remove_occupied_space(end_position)

        # Update GameBoard and position of moving Piece
        board.remove_piece(start_position)
        board.place_piece(end_position, player_piece)
        player_piece.set_position(end_position)
        player.remove_occupied_space(start_position)
        player.add_occupied_space(end_position)

    def move_leaves_player_in_check(self, test_game, test_start_position, test_end_position):
        """
        Simulates the parameterized Piece movement on a copy of the current game state. Returns True if the move
        leaves the Player in check or False if not.
        """

        test_board = test_game.get_board()
        test_player_piece = test_board.get_piece_at_coord(test_start_position)
        test_player = test_player_piece.get_player()
        test_opponent = test_game.get_players()[test_player.get_opponent_color()]
        test_opponent_piece = test_board.get_piece_at_coord(test_end_position)

        self.update_board(test_board, test_player, test_opponent, test_player_piece, test_opponent_piece,
                          test_start_position, test_end_position)

        if test_player.get_general().get_position() in test_opponent.get_threat_range(test_board):
            return True
        else:
            return False

    def verify_checkmate(self, player):
        """
        Takes a parameterized Player currently in check and iterates over their collection of Pieces, determining valid
        moves for each Piece. Creates a copy of the current game state and simulates each movement, verifying whether
        the move leaves the Player in check. If the move does not leave the Player in check, returns False. If all moves
        have been exhausted, returns True, indicating checkmate.
        """

        for piece in player.get_pieces():

            for move in piece.get_move_range(self._board):

                # Create copy of the current game state and simulate movement. If a move does not leave the Player in
                # check, then the Player has a move available to counter the check, nullifying the checkmate condition.
                test_game = copy.deepcopy(self)
                start_position = piece.get_position()
                if self.move_leaves_player_in_check(test_game, start_position, move) is False:
                    return False

        return True

    def convert_algebraic_notation(self, alg_not):
        """
        Takes a string in algebraic notation, converts it to a coordinate tuple, and returns the tuple.
        """

        x_coord = self._algebraic_notation[alg_not[0]]

        if len(alg_not) < 3:
            y_coord = self._algebraic_notation[alg_not[1]]

        # If second character in string is 2 digits in length, concatenate the second and third character
        else:
            y_coord = self._algebraic_notation[alg_not[1] + alg_not[2]]

        return x_coord, y_coord

    def get_board(self):
        """
        Returns the Game's GameBoard.
        """
        return self._board

    def get_players(self):
        """
        Returns the Game's Player dictionary.
        """
        return self._players

    def print_board(self):
        """
        Prints the game board. For debugging purposes only.
        """
        self._board.print_board()


class Player:
    """
    Represents a Player object. Has a color, an opponent color, a list of Pieces, a set of occupied Spaces, and a set of
    threatened Spaces. Has methods to get the Player's color, get their opponent's color, get their list of Pieces,
    remove a Piece from their collection, get their General Piece, get whether their General Piece is in check, set
    whether their General Piece is in check, get their threat range, add to and remove from their set of occupied
    Spaces, and get their set of occupied Spaces.
    """

    def __init__(self, color):
        """
        Initializes a Player with the parameterized color. Also has initial attributes for their opponent's color, a
        list of Pieces, a set of occupied Spaces, and a set of threatened Spaces.
        """
        self._color = color
        self._opponent_color = None
        self._pieces = []
        self._occupied_spaces = set()
        self._threat_range = set()

        # Instantiate BoardPieces at the specified coordinates depending on Player color, add them to the Player's
        # list of Pieces, assign the Player to to the Piece, and adds the Piece's position to the Player's set of
        # occupied Spaces.
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
        Returns the Player's color.
        """
        return self._color

    def get_opponent_color(self):
        """
        Returns the Player's opponent's color.
        """
        return self._opponent_color

    def get_pieces(self):
        """
        Returns the Player's list of Pieces.
        """
        return self._pieces

    def remove_piece(self, piece):
        """
        Removes the parameterized Piece from the Player's list of Pieces.
        """
        self._pieces.remove(piece)

    def get_general(self):
        """
        Returns the instance of the Player's General Piece.
        """
        return self._pieces[0]

    def get_is_in_check(self):
        """
        Returns whether the Player's General Piece is in check.
        """
        return self.get_general().get_is_in_check()

    def set_is_in_check(self, bool_val):
        """
        Sets whether the Player's General Piece is in check based on the parameterized boolean value.
        """
        self.get_general().set_is_in_check(bool_val)

    def get_threat_range(self, board):
        """
        Takes the parameterized GameBoard and returns a set of all of the Player's threatened Spaces.
        """
        self._threat_range.clear()

        # Iterate through Player's list of Pieces, get the Piece's set of possible moves, and adds it to the total set
        # of threatened coordinates via the set union operation
        for piece in self._pieces:
            self._threat_range = self._threat_range | piece.get_move_range(board)

        return self._threat_range

    def add_occupied_space(self, coord):
        """
        Takes the parameterized coordinate and adds it to the Player's set of occupied Spaces.
        """
        self._occupied_spaces.add(coord)

    def remove_occupied_space(self, coord):
        """
        Takes the parameterized coordinate and removes it from the Player's set of occupied Spaces.
        """
        self._occupied_spaces.remove(coord)

    def get_occupied_spaces(self):
        """
        Returns the Player's set of occupied Spaces.
        """
        return self._occupied_spaces


class GameBoard:
    """
    Represents a GameBoard object. Has a 9 x 10 2D array of spaces, a set of all Space coordinates on the board,
    a set of all available (i.e. unoccupied) Spaces, a set of defining the Board's Palace areas, and a set defining
    the Spaces in the Board's Palace areas connected by diagonals. Also has methods to place a Piece on the Board,
    remove a Piece from the Board, get the set of all Board Spaces, get the set of all available Spaces, get the set
    of all occupied Spaces, get the set of all Palace coordinates, get the set of all Palace coordinates connected by
    diagonal pathways, get the Piece at a specified coordinate, and print the GameBoard.
    """
    def __init__(self):
        """
        Initializes the GameBoard. Has a 9 x 10 2D array of spaces, a set of all Space coordinates on the board,
        a set of all available (i.e. unoccupied) Spaces, a set of defining the Board's Palace areas, and a set defining
        the Spaces in the Board's Palace areas connected by diagonals as initial attributes.
        """
        self._spaces = []
        self._x_length = 9
        self._y_length = 10
        self._all_spaces = set()
        self._available_spaces = set()
        self._palace_spaces = set()
        self._palace_diagonals = set()

        # Populate GameBoard, instantiating empty Space objects at each coordinate and adding the coordinate to the
        # set of all Spaces.
        for column in range(self._x_length):
            self._spaces.append([])

            for row in range(self._y_length):
                coord = (column, row)
                self._spaces[column].append(Space(coord))
                self._all_spaces.add(coord)

        self._available_spaces = set(self._all_spaces)

        # Define Palace Spaces as well as those connected by diagonal pathways. Adds these coordinates to the
        # corresponding data member sets
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

    def __repr__(self):
        return "GameBoard"

    def place_piece(self, coord, piece):
        """
        Takes a coordinate and Piece object as parameters, places the Piece on that Space, and updates the set of
        available Spaces.
        """
        x_coord, y_coord = coord
        space = self._spaces[x_coord][y_coord]
        space.place_piece(piece)
        self._available_spaces.remove(coord)

    def remove_piece(self, coord):
        """
        Removes the Piece from the parameterized Coordinate and updates the set of available Spaces.
        """
        x_coord, y_coord = coord
        space = self._spaces[x_coord][y_coord]
        space.remove_piece()
        self._available_spaces.add(coord)

    def get_all_spaces(self):
        """
        Returns the set of all coordinates within the Board's boundaries.
        """
        return self._all_spaces

    def get_available_spaces(self):
        """
        Returns the set of all available (i.e. unoccupied) Spaces.
        """
        return self._available_spaces

    def get_occupied_spaces(self):
        """
        Returns the set of all currently occupied Spaces.
        """
        # Set difference of all Spaces on the Board and available Spaces = occupied spaces
        return self._all_spaces - self._available_spaces

    def get_palace_spaces(self):
        """
        Returns the set of all Palace Spaces.
        """
        return self._palace_spaces

    def get_palace_diagonals(self):
        """
        Returns the set of all Palace Spaces connected by diagonal pathways.
        """
        return self._palace_diagonals

    def get_piece_at_coord(self, coord):
        """
        Returns the instance of the Piece object at the parameterized coordinate.
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
    Represents a Space object on the GameBoard. Has a coordinate and occupant Piece as attributes. Also has methods to
    place a Piece on itself, remove a Piece from itself, and get the Piece currently occupying it.
    """
    def __init__(self, coord):
        """
        Instantiates an empty Space on the GameBoard at the parameterized coordinate. Has a unique coordinate as well as
        a Piece currently occupying it (set to None) as initial attributes.
        """
        self._coord = coord
        self._piece = None

    def __repr__(self):
        if self._piece is None:
            return "Square(" + repr(self._coord) + ", " + repr(self._piece) + ")"
        else:
            return self._piece

    def __str__(self):
        """
        String representation of either an empty Space or the Space's occupying Piece when printed on the GameBoard.
        """
        if self._piece is None:
            return " . "
        else:
            return str(self._piece)

    def place_piece(self, piece):
        """
        Takes a parameterized Piece and places it on itself.
        """
        self._piece = piece

    def remove_piece(self):
        """
        Clears the Space of any occupying Pieces.
        """
        self._piece = None

    def get_piece(self):
        """
        Returns the Piece (or lack thereof) currently occupying the Space.
        """
        return self._piece


class PalaceSpace(Space):
    """
    Represents a PalaceSpace object on the GameBoard defining the Palace areas. Inherits from Space.
    """

    def __repr__(self):
        if self._piece is None:
            return "PalaceSquare(" + repr(self._coord) + ", " + repr(self._piece) + ")"
        else:
            return self._piece

    def __str__(self):
        """
        String representation of either an empty PalaceSpace or the PalaceSpace's occupying Piece when printed on the
        GameBoard.
        """
        if self._piece is None:
            return " * "
        else:
            return str(self._piece)


class BoardPiece:
    """
    Represents a generic BoardPiece on the GameBoard. Has a Player object as an attribute, a color corresponding with
    their Player, a tuple coordinate position, and a set of possible moves relative to its position. Also has methods to
    set its current position, get its current position, set its Player, and get its Player.
    """

    def __init__(self, position):
        """
        Initializes the BoardPiece at the parameterized position. Has a Player object and corresponding color
        (initialized to None) as well as a position and set of possible moves as initial attributes.
        """
        self._player = None
        self._color = None
        self._position = position
        self._move_range = set()

    def set_position(self, coord):
        """
        Takes the parameterized coordinate and uses it to update the Piece's current position.
        """
        self._position = coord

    def get_position(self):
        """
        Returns the Piece's current position.
        """
        return self._position

    def set_player(self, player):
        """
        Sets the Player that the Piece belongs to along with its corresponding color.
        """
        self._player = player
        self._color = player.get_color()

    def get_player(self):
        """
        Returns the Player that the Piece belongs to.
        """
        return self._player


class General(BoardPiece):
    """
    Represents a General-rank BoardPiece. Inherits from BoardPiece. Has an additional boolean attribute for whether the
    General is in check. Also has methods to set and get whether the General is in check as well as a method to get its
    set of available moves.
    """

    def __init__(self, position):
        """
        Initializes a General with the parameterized position that inherits initial attributes of a generic BoardPiece.
        Also has a boolean attribute for whether the General is in check.
        """
        super().__init__(position)
        self._is_in_check = False

    def __repr__(self):
        return "General(" + repr(self._color) + ", " + repr(self._position) + ")"

    def __str__(self):
        """
        String representation of the General when printed on the GameBoard.
        """
        return self._color[0].upper() + "GN"

    def get_move_range(self, board):
        """
        Takes the parameterized GameBoard, then generates and returns the set of all possible moves currently available
        relative to the General's position.
        """

        self._move_range.clear()

        palace_spaces = board.get_palace_spaces()
        palace_diagonals = board.get_palace_diagonals()
        allied_spaces = self._player.get_occupied_spaces()
        x_pos, y_pos = self._position

        # Defines both orthogonal and diagonal movement when on Palace coordinate connected by diagonal pathways
        if self._position in palace_diagonals:

            for x_coord in range(x_pos - 1, x_pos + 2):
                for y_coord in range(y_pos - 1, y_pos + 2):

                    # If the coordinate is within the Palace and is not occupied by an allied Piece
                    if (x_coord, y_coord) in palace_spaces - allied_spaces:
                        self._move_range.add((x_coord, y_coord))

        # If not on Palace coordinate connected by diagonal pathways, can only move orthogonally
        else:

            for x_coord in range(x_pos - 1, x_pos + 2):

                # If the coordinate is within the Palace and is not occupied by an allied Piece
                if (x_coord, y_pos) in palace_spaces - allied_spaces:
                    self._move_range.add((x_coord, y_pos))

            for y_coord in range(y_pos - 1, y_pos + 2):

                # If the coordinate is within the Palace and is not occupied by an allied Piece
                if (x_pos, y_coord) in palace_spaces - allied_spaces:
                    self._move_range.add((x_pos, y_coord))

        return self._move_range

    def set_is_in_check(self, bool_val):
        """
        Takes a parameterized boolean value and uses it to set whether the General is in check.
        """
        self._is_in_check = bool_val

    def get_is_in_check(self):
        """
        Returns whether the General is in check.
        """
        return self._is_in_check


class Guard(BoardPiece):
    """
    Represents a Guard-rank BoardPiece. Inherits from BoardPiece. Has an additional method to get its set of available
    moves.
    """

    def __repr__(self):
        return "Guard(" + repr(self._color) + ", " + repr(self._position) + ")"

    def __str__(self):
        """
        String representation of the General when printed on the GameBoard.
        """
        return self._color[0].upper() + "GD"

    def get_move_range(self, board):
        """
        Takes the parameterized GameBoard, then generates and returns the set of all possible moves currently available
        relative to the Guard's position.
        """

        self._move_range.clear()

        palace_spaces = board.get_palace_spaces()
        palace_diagonals = board.get_palace_diagonals()
        allied_spaces = self._player.get_occupied_spaces()
        x_pos, y_pos = self._position

        # Defines both orthogonal and diagonal movement when on Palace coordinate connected by diagonal pathways
        if self._position in palace_diagonals:
            for x_coord in range(x_pos - 1, x_pos + 2):
                for y_coord in range(y_pos - 1, y_pos + 2):

                    # If the coordinate is within the Palace and is not occupied by an allied Piece
                    if (x_coord, y_coord) in palace_spaces - allied_spaces:
                        self._move_range.add((x_coord, y_coord))

        # If not on Palace coordinate connected by diagonal pathways, can only move orthogonally
        else:
            for x_coord in range(x_pos - 1, x_pos + 2):

                # If the coordinate is within the Palace and is not occupied by an allied Piece
                if (x_coord, y_pos) in palace_spaces - allied_spaces:
                    self._move_range.add((x_coord, y_pos))

            for y_coord in range(y_pos - 1, y_pos + 2):

                # If the coordinate is within the Palace and is not occupied by an allied Piece
                if (x_pos, y_coord) in palace_spaces - allied_spaces:
                    self._move_range.add((x_pos, y_coord))

        return self._move_range


class Horse(BoardPiece):
    """
    Represents a Horse-rank BoardPiece. Inherits from BoardPiece. Has an additional method to get its set of available
    moves.
    """

    def __repr__(self):
        return "Horse(" + repr(self._color) + ", " + repr(self._position) + ")"

    def __str__(self):
        """
        String representation of the General when printed on the GameBoard.
        """
        return self._color[0].upper() + "HS"

    def get_move_range(self, board):
        """
        Takes the parameterized GameBoard, then generates and returns the set of all possible moves currently available
        relative to the Horse's position.
        """

        self._move_range.clear()

        all_spaces = board.get_all_spaces()
        allied_spaces = self._player.get_occupied_spaces()
        x_pos, y_pos = self._position

        # Evaluates available spaces if Horse moves due west or due east from its current position. Horse moves one
        # space forward then one space diagonally outward. Stops if there is an obstruction in the path.
        for x_coord in range(x_pos - 1, x_pos + 2, 2):
            if (x_coord, y_pos) in all_spaces and board.get_piece_at_coord((x_coord, y_pos)) is None:
                for y_coord in range(y_pos - 1, y_pos + 2, 2):

                    if x_coord < x_pos:
                        x_offset = -1
                    else:
                        x_offset = 1

                    # If the coordinate is within the Board's boundaries and is not occupied by an allied Piece
                    if (x_coord + x_offset, y_coord) in all_spaces - allied_spaces:
                        self._move_range.add((x_coord + x_offset, y_coord))

        # Evaluates available spaces if Horse moves due north or due south from its current position. Horse moves one
        # space forward then one space diagonally outward. Stops if there is an obstruction in the path.
        for y_coord in range(y_pos - 1, y_pos + 2, 2):
            if (x_pos, y_coord) in all_spaces and board.get_piece_at_coord((x_pos, y_coord)) is None:
                for x_coord in range(x_pos - 1, x_pos + 2, 2):

                    if y_coord < y_pos:
                        y_offset = -1
                    else:
                        y_offset = 1

                    # If the coordinate is within the Board's boundaries and is not occupied by an allied Piece
                    if (x_coord, y_coord + y_offset) in all_spaces - allied_spaces:
                        self._move_range.add((x_coord, y_coord + y_offset))

        return self._move_range


class Elephant(BoardPiece):
    """
    Represents an Elephant-rank BoardPiece. Inherits from BoardPiece. Has an additional method to get its set of
    available moves.
    """

    def __repr__(self):
        return "Elephant(" + repr(self._color) + ", " + repr(self._position) + ")"

    def __str__(self):
        """
        String representation of the General when printed on the GameBoard.
        """
        return self._color[0].upper() + "EP"

    def get_move_range(self, board):
        """
        Takes the parameterized GameBoard, then generates and returns the set of all possible moves currently available
        relative to the Elephant's position.
        """

        self._move_range.clear()

        all_spaces = board.get_all_spaces()
        allied_spaces = self._player.get_occupied_spaces()
        x_pos, y_pos = self._position

        # Evaluates available spaces if Elephant moves due west or due east from its current position. Elephant moves
        # one space forward then two spaces diagonally outward. Stops if there is an obstruction in the path.
        for x_coord in range(x_pos - 1, x_pos + 2, 2):

            if (x_coord, y_pos) in all_spaces and board.get_piece_at_coord((x_coord, y_pos)) is None:
                for y_coord in range(y_pos - 1, y_pos + 2, 2):

                    if x_coord < x_pos:
                        x_offset = -1

                    else:
                        x_offset = 1

                    if (x_coord + x_offset, y_coord) in all_spaces and \
                            board.get_piece_at_coord((x_coord + x_offset, y_coord)) is None:
                        for y_coord in range(y_pos - 2, y_pos + 3, 4):

                            if x_coord < x_pos:
                                x_offset = -2

                            else:
                                x_offset = 2

                            # If the coordinate is within the Board's boundaries and is not occupied by an allied Piece
                            if (x_coord + x_offset, y_coord) in all_spaces - allied_spaces:
                                self._move_range.add((x_coord + x_offset, y_coord))

        # Evaluates available spaces if Elephant moves due north or due south from its current position. Elephant moves
        # one space forward then two spaces diagonally outward. Stops if there is an obstruction in the path.
        for y_coord in range(y_pos - 1, y_pos + 2, 2):
            if (x_pos, y_coord) in all_spaces and board.get_piece_at_coord((x_pos, y_coord)) is None:
                for x_coord in range(x_pos - 1, x_pos + 2, 2):

                    if y_coord < y_pos:
                        y_offset = -1

                    else:
                        y_offset = 1

                    if (x_coord, y_coord + y_offset) in all_spaces and \
                            board.get_piece_at_coord((x_coord, y_coord + y_offset)) is None:
                        for x_coord in range(x_pos - 2, x_pos + 3, 4):

                            if y_coord < y_pos:
                                y_offset = -2

                            else:
                                y_offset = 2

                            # If the coordinate is within the Board's boundaries and is not occupied by an allied Piece
                            if (x_coord, y_coord + y_offset) in all_spaces - allied_spaces:
                                self._move_range.add((x_coord, y_coord + y_offset))

        return self._move_range


class Chariot(BoardPiece):
    """
    Represents a Chariot-rank BoardPiece. Inherits from BoardPiece. Has an additional method to get its set of available
    moves.
    """

    def __repr__(self):
        return "Chariot(" + repr(self._color) + ", " + repr(self._position) + ")"

    def __str__(self):
        """
        String representation of the General when printed on the GameBoard.
        """
        return self._color[0].upper() + "CH"

    def get_move_range(self, board):
        """
        Takes the parameterized GameBoard, then generates and returns the set of all possible moves currently available
        relative to the Chariot's position.
        """

        self._move_range.clear()

        all_spaces = board.get_all_spaces()
        palace_diagonals = board.get_palace_diagonals()
        allied_spaces = self._player.get_occupied_spaces()
        x_pos, y_pos = self._position

        # Chariot can move any number of spaces orthogonally until it reaches an obstruction

        # Check Spaces due west
        x_offset = -1
        while (x_pos + x_offset, y_pos) in all_spaces:
            piece = board.get_piece_at_coord((x_pos + x_offset, y_pos))
            if piece is not None:

                # If the obstructing Piece is not an ally, adds it to the set of available moves
                if (x_pos + x_offset, y_pos) not in allied_spaces:
                    self._move_range.add((x_pos + x_offset, y_pos))
                break

            # Adds the empty Space to the list set of available moves
            self._move_range.add((x_pos + x_offset, y_pos))
            x_offset -= 1

        # Check Spaces due east
        x_offset = 1
        while (x_pos + x_offset, y_pos) in all_spaces:
            piece = board.get_piece_at_coord((x_pos + x_offset, y_pos))
            if piece is not None:

                # If the obstructing Piece is not an ally, adds it to the set of available moves
                if (x_pos + x_offset, y_pos) not in allied_spaces:
                    self._move_range.add((x_pos + x_offset, y_pos))
                break

            # Adds the empty Space to the list set of available moves
            self._move_range.add((x_pos + x_offset, y_pos))
            x_offset += 1

        # Check Spaces due north
        y_offset = -1
        while (x_pos, y_pos + y_offset) in all_spaces:
            piece = board.get_piece_at_coord((x_pos, y_pos + y_offset))
            if piece is not None:

                # If the obstructing Piece is not an ally, adds it to the set of available moves
                if (x_pos, y_pos + y_offset) not in allied_spaces:
                    self._move_range.add((x_pos, y_pos + y_offset))
                break

            # Adds the empty Space to the list set of available moves
            self._move_range.add((x_pos, y_pos + y_offset))
            y_offset -= 1

        # Check Spaces due south
        y_offset = 1
        while (x_pos, y_pos + y_offset) in all_spaces:
            piece = board.get_piece_at_coord((x_pos, y_pos + y_offset))
            if piece is not None:

                # If the obstructing Piece is not an ally, adds it to the set of available moves
                if (x_pos, y_pos + y_offset) not in allied_spaces:
                    self._move_range.add((x_pos, y_pos + y_offset))
                break

            # Adds the empty Space to the list set of available moves
            self._move_range.add((x_pos, y_pos + y_offset))
            y_offset += 1

        # Palace-augmented movement when Chariot is on Palace Space connected by diagonal pathways
        if self._position in palace_diagonals:

            # Piece is in center of Palace
            if x_pos == 4:
                for x_coord in range(x_pos - 1, x_pos + 2):
                    for y_coord in range(y_pos - 1, y_pos + 2):
                        if abs(x_coord - x_pos) == abs(y_coord - y_pos):

                            piece = board.get_piece_at_coord((x_coord, y_coord))

                            # If the corners of the Palace are empty or are not occupied by allies, add them to the
                            # set of available moves
                            if piece is None or (x_coord, y_coord) not in allied_spaces:
                                self._move_range.add((x_coord, y_coord))

            # Piece is in corner of Palace
            else:

                palace_center = None
                # Find Palace center relative to position
                for x_coord in range(x_pos - 1, x_pos + 2):
                    for y_coord in range(y_pos - 1, y_pos + 2):

                        # Palace center found
                        if abs(x_coord - x_pos) == abs(y_coord - y_pos) and (x_coord, y_coord) in palace_diagonals and \
                                (x_coord, y_coord) != self._position:

                            palace_center = (x_coord, y_coord)
                            break

                # Determine whether to iterate spaces northwest, southwest, northeast, southeast of current position
                # based on Palace center's direction relative to position.
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

                        # If the obstructing Piece is not an ally, adds it to the set of available moves
                        if (x_pos + x_offset, y_pos + y_offset) not in allied_spaces:
                            self._move_range.add((x_pos + x_offset, y_pos + y_offset))
                        break

                    # Adds the empty Space to the list set of available moves
                    self._move_range.add((x_pos + x_offset, y_pos + y_offset))
                    x_offset += x_offset
                    y_offset += y_offset

        return self._move_range


class Cannon(BoardPiece):
    """
    Represents a Cannon-rank BoardPiece. Inherits from BoardPiece. Has an additional method to get its set of available
    moves.
    """

    def __repr__(self):
        return "Cannon(" + repr(self._color) + ", " + repr(self._position) + ")"

    def __str__(self):
        """
        String representation of the General when printed on the GameBoard.
        """
        return self._color[0].upper() + "CN"

    def get_move_range(self, board):
        """
        Takes the parameterized GameBoard, then generates and returns the set of all possible moves currently available
        relative to the Cannon's position.
        """

        self._move_range.clear()

        all_spaces = board.get_all_spaces()
        palace_diagonals = board.get_palace_diagonals()
        allied_spaces = self._player.get_occupied_spaces()
        x_pos, y_pos = self._position

        # Chariot can move any number of spaces orthogonally provided there is exactly one non-Cannon Piece between
        # itself and its destination. It may not jump over nor capture other Cannons.

        # Check Spaces due west
        x_offset = -1
        pieces_between = 0
        while (x_pos + x_offset, y_pos) in all_spaces:

            piece = board.get_piece_at_coord((x_pos + x_offset, y_pos))

            if piece is not None:
                if pieces_between == 1 or isinstance(piece, Cannon):

                    # If the obstruction is neither an allied Piece nor a Cannon, add the Space to the set of available
                    # moves
                    if (x_pos + x_offset, y_pos) not in allied_spaces and isinstance(piece, Cannon) is False:
                        self._move_range.add((x_pos + x_offset, y_pos))
                    break
                pieces_between += 1

            else:
                if pieces_between == 1:

                    # If the Space is unoccupied and there is one Piece between the Cannon and destination, add the
                    # Space to the set of available moves
                    self._move_range.add((x_pos + x_offset, y_pos))
            x_offset -= 1

        # Check Spaces due east
        x_offset = 1
        pieces_between = 0
        while (x_pos + x_offset, y_pos) in all_spaces:

            piece = board.get_piece_at_coord((x_pos + x_offset, y_pos))

            if piece is not None:
                if pieces_between == 1 or isinstance(piece, Cannon):

                    # If the obstruction is neither an allied Piece nor a Cannon, add the Space to the set of available
                    # moves
                    if (x_pos + x_offset, y_pos) not in allied_spaces and isinstance(piece, Cannon) is False:
                        self._move_range.add((x_pos + x_offset, y_pos))
                    break
                pieces_between += 1

            else:
                if pieces_between == 1:

                    # If the Space is unoccupied and there is one Piece between the Cannon and destination, add the
                    # Space to the set of available moves
                    self._move_range.add((x_pos + x_offset, y_pos))
            x_offset += 1

        # Check Spaces due north
        y_offset = -1
        pieces_between = 0
        while (x_pos, y_pos + y_offset) in all_spaces:

            piece = board.get_piece_at_coord((x_pos, y_pos + y_offset))

            if piece is not None:
                if pieces_between == 1 or isinstance(piece, Cannon):

                    # If the obstruction is neither an allied Piece nor a Cannon, add the Space to the set of available
                    # moves
                    if (x_pos, y_pos + y_offset) not in allied_spaces and isinstance(piece, Cannon) is False:
                        self._move_range.add((x_pos, y_pos + y_offset))
                    break
                pieces_between += 1

            else:
                if pieces_between == 1:

                    # If the Space is unoccupied and there is one Piece between the Cannon and destination, add the
                    # Space to the set of available moves
                    self._move_range.add((x_pos, y_pos + y_offset))
            y_offset -= 1

        # Check Spaces due south
        y_offset = 1
        pieces_between = 0
        while (x_pos, y_pos + y_offset) in all_spaces:

            piece = board.get_piece_at_coord((x_pos, y_pos + y_offset))

            if piece is not None:
                if pieces_between == 1 or isinstance(piece, Cannon):

                    # If the obstruction is neither an allied Piece nor a Cannon, add the Space to the set of available
                    # moves
                    if (x_pos, y_pos + y_offset) not in allied_spaces and isinstance(piece, Cannon) is False:
                        self._move_range.add((x_pos, y_pos + y_offset))
                    break
                pieces_between += 1

            else:
                if pieces_between == 1:

                    # If the Space is unoccupied and there is one Piece between the Cannon and destination, add the
                    # Space to the set of available moves
                    self._move_range.add((x_pos, y_pos + y_offset))
            y_offset += 1

        # Palace-augmented diagonal movement when Cannon is in Palace (can only happen when Cannon is on a Palace
        # corner)
        if self._position in palace_diagonals:

            palace_center = None

            # Find Palace center relative to current position
            for x_coord in range(x_pos - 1, x_pos + 2):
                for y_coord in range(y_pos - 1, y_pos + 2):

                    # Palace center found
                    if abs(x_coord - x_pos) == abs(y_coord - y_pos) and (x_coord, y_coord) in palace_diagonals and \
                            (x_coord, y_coord) != self._position:
                        palace_center = (x_coord, y_coord)
                        break

            piece_at_center = board.get_piece_at_coord(palace_center)

            # Cannon can only jump diagonally within Palace if center space is occupied by a non-Cannon Piece
            if piece_at_center is not None and isinstance(piece_at_center, Cannon) is False:

                # Find Palace corner diagonally from current position based on Palace center's position relative to
                # the current position
                if palace_center[0] < x_pos:
                    x_offset = -2
                else:
                    x_offset = 2

                if palace_center[1] < y_pos:
                    y_offset = -2
                else:
                    y_offset = 2

                # If the corner destination is not occupied by an allied Piece, add the destination to the set of
                # available moves
                if (x_pos + x_offset, y_pos + y_offset) not in allied_spaces:
                    self._move_range.add((x_pos + x_offset, y_pos + y_offset))

        return self._move_range


class Soldier(BoardPiece):
    """
    Represents a Soldier-rank BoardPiece. Inherits from BoardPiece. Has an additional method to get its set of available
    moves.
    """

    def __repr__(self):
        return "Soldier(" + repr(self._color) + ", " + repr(self._position) + ")"

    def __str__(self):
        """
        String representation of the General when printed on the GameBoard.
        """
        return self._color[0].upper() + "SD"

    def get_move_range(self, board):
        """
        Takes the parameterized GameBoard, then generates and returns the set of all possible moves currently available
        relative to the Soldier's position.
        """

        self._move_range.clear()

        all_spaces = board.get_all_spaces()
        palace_diagonals = board.get_palace_diagonals()
        allied_spaces = self._player.get_occupied_spaces()
        x_pos, y_pos = self._position

        # Soldier may only move one space horizontally or forward to the opponent's side of the Board. May move along
        # diagonal pathways within Palaces as well

        # Set forward movement based on color
        if self._color == "blue":
            y_offset = -1

        else:
            y_offset = 1

        # Check horizontal movement
        for x_coord in range(x_pos - 1, x_pos + 2):

            # If the coordinate is within the boundaries of the Board and is not occupied by an allied Piece, add it
            # to the set of available moves
            if (x_coord, y_pos) in all_spaces - allied_spaces:
                self._move_range.add((x_coord, y_pos))

        # Check forward movement. If the coordinate is within the boundaries of the Board and is not occupied by an
        # allied Piece, add it to the set of available moves
        if (x_pos, y_pos + y_offset) in all_spaces - allied_spaces:
            self._move_range.add((x_pos, y_pos + y_offset))

        # Diagonal movement augmentation within Palace
        if self._position in palace_diagonals:
            for x_coord in range(x_pos - 1, x_pos + 2):

                # If the coordinate is on a Palace Space connected by diagonal pathways and is not occupied by an
                # allied piece, add it to the set of available moves
                if (x_coord, y_pos + y_offset) in palace_diagonals - allied_spaces:
                    self._move_range.add((x_coord, y_pos + y_offset))

        return self._move_range
