# Author: George Kochera
# Date: 3/12/2020
# Description: Portfolio Project - XiangqiGame.py

# This module is the final project for CS162. It encapsulates a demonstration of knowledge attained through the past
# 20 weeks. This module in particular is an engine for a Chinese chess game known as Xiangqi. The rules are quite
# similar to American chess but differ in a few specific regards. Two resources were used to create this game
# engine. The first is from Wikipedia which was also provided in the readme. It is located at (
# https://en.wikipedia.org/wiki/Xiangqi). The second website is called AncientChess and it can be located at (
# http://ancientchess.com/page/play-xiangqi.htm).
#
# To begin a game, simply instantiate a new XiangqiGame object. The board is set when the object is constructed. The
# key commands to use are make_move() which takes two strings in the form of algebraic notation: the piece to move,
# and where to move it to. The second command is get_game_state(). It returns whether the game is still unfinished or
# if it has been won (and by whom). The last key command is is_in_check(). It takes one argument as a string,
# either 'Black' or 'Red' and will indicate if that person's general is in a check condition. It evaluates the board
# at the time the method is called so the status is not 'stale'.
#
# Due to the size of this project, this description is far from comprehensive. TA's, instructors and other readers
# are encouraged to review the assocated comments and docstrings for further details on the application.
#
# IMPORTANT:
# The term 'player' means the color of the team. 'player' always refers to either the string value 'Red'
# or 'Black'.
#
# The term 'square' is an informal data structure that is used THORUGHOUT this code. It refers to the
# string that holds the position in algebraic notation. 'e1', 'f9', 'c3', and 'i10' are all 'square's.

# --- BEGIN APPLICATION CODE ---

# Regular expressions are used to validate user input so that library is imported.
import re

# Module Constants that are used to traverse between algebraic notation and column/row tuples a.k.a. array indices.
# The squares that define the palace for each player are also defined here.
COLUMN_KEY = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8}
ROW_KEY = {1: 9, 2: 8, 3: 7, 4: 6, 5: 5, 6: 4, 7: 3, 8: 2, 9: 1, 10: 0}
FILE_KEY = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i'}
RANK_KEY = {9: '1', 8: '2', 7: '3', 6: '4', 5: '5', 4: '6', 3: '7', 2: '8', 1: '9', 0: '10'}
BLACK_PALACE = ('d10', 'e10', 'f10', 'd9', 'e9', 'f9', 'd8', 'e8', 'f8')
RED_PALACE = ('d1', 'e1', 'f1', 'd2', 'e2', 'f2', 'd3', 'e3', 'f3')
SQUARE_REGEX = re.compile("[a-i]{1}[1-9]{1}0?")


# These methods are static methods. They do not require a class to run. They do serve as helper functions to perform
# specific tasks for objects.


def algebraic_notation_to_indices(square):
    """
    Converts from algebraic notation to column/row index. Also checks for invalid and out-of-bounds values. Will
    return false when this happens.
    """
    if not SQUARE_REGEX.match(square):
        return False
    try:
        column = COLUMN_KEY[square[:1]]
        row = ROW_KEY[int(square[1:])]
    except KeyError:
        return False
    return column, row


def indices_to_algebraic_notation(column, row):
    """
    Converts from a column/row index to a string in algebraic notation. Will return false if an out of bounds
    value is attempted.
    """
    try:
        rank = RANK_KEY[row]
        file = FILE_KEY[column]
    except KeyError:
        return False
    return file + rank


def is_backwards_move(moving_from_square, moving_to_square, team):
    """Simply checks for a backward movement depending on which player is making the move."""
    if team == 'Black':
        if algebraic_notation_to_indices(moving_from_square)[1] > algebraic_notation_to_indices(moving_to_square)[1]:
            return True
        return False
    else:
        if algebraic_notation_to_indices(moving_from_square)[1] < algebraic_notation_to_indices(moving_to_square)[1]:
            return True
        return False


def is_vertical_or_horizontal_move(moving_from_square, moving_to_square):
    """Enforces both vertical and horizontal movement. Disallows diagonal movement."""
    return is_vertical_move(moving_from_square, moving_to_square) or \
           is_horizontal_move(moving_from_square, moving_to_square)


def is_vertical_move(moving_from_square, moving_to_square):
    """Checks to see if the move is within a single column (vertical)."""
    column_from = algebraic_notation_to_indices(moving_from_square)[0]
    column_to = algebraic_notation_to_indices(moving_to_square)[0]
    if column_from == column_to:
        return True
    return False


def is_horizontal_move(moving_from_square, moving_to_square):
    """Checks to see if the move is within a single row (horizontal)."""
    row_from = algebraic_notation_to_indices(moving_from_square)[1]
    row_to = algebraic_notation_to_indices(moving_to_square)[1]
    if row_from == row_to:
        return True
    return False


def piece_linear_path_helper(moving_from_square, moving_to_square):
    """
    Creates a list of every square from one square to another (inclusive) which starts with the from square at
    index 0. Used by functions such as can_generals_not_see_each_other() to see which pieces exist within the same file.
    """
    column_from, row_from = algebraic_notation_to_indices(moving_from_square)
    column_to, row_to = algebraic_notation_to_indices(moving_to_square)

    squares_between_piece_and_target = []

    # When the column is equal, we search within the column and work either up or down depending on the arguments.
    if column_from == column_to:
        if row_from > row_to:
            for space in range(row_to, row_from + 1):
                squares_between_piece_and_target.insert(0, indices_to_algebraic_notation(column_from, space))
        else:
            for space in range(row_from, row_to + 1):
                squares_between_piece_and_target.append(indices_to_algebraic_notation(column_from, space))

    # When the row is equal, we search within the row and work right or left based on the arguments passed.
    else:
        if column_from > column_to:
            for space in range(column_to, column_from + 1):
                squares_between_piece_and_target.insert(0, indices_to_algebraic_notation(space, row_from))
        else:
            for space in range(column_from, column_to + 1):
                squares_between_piece_and_target.append(indices_to_algebraic_notation(space, row_from))

    # We return a list of squares from moving_from_square to moving_to_square (inclusive). Index 0 is
    # moving_from_square.
    return squares_between_piece_and_target


def generate_threat_dictionary(game, current_player):
    """
    Helper function that scans the entire game board for pieces that belong to the opponent and returns a dictionary
    containing all the possible moves every opponent piece can make. Keys are the GamePiece objects/Values are
    lists of the possible moves for that GamePiece.
    """
    threats = dict()
    board = game.get_game_board()

    # Scan every square on the board for a piece that does not belong to the current player. When one is found,
    # the list possible moves for that piece is called, which returns a list of possible moves that piece can make.
    for row in board:
        for piece in row:
            if piece.get_team() is not current_player:
                if piece.get_team() is not None:
                    threats[piece] = piece.list_possible_moves(game)

    # Return the dictionary containing all of the opponents possible moves when done.
    return threats


def try_move(moving_from_square, moving_to_square, game, evaluate_for_opposing_general=False):
    """
    This function executes when is_in_check() asks a piece to try a specific move. The basic premise of this function
    is to move the piece, see if the current player is in check (by evaluating for threats), or becomes in check,
    and then return the pieces to their starting position. If the move results in a check condition: False is
    returned otherwise True is returned.
    """

    # Get the piece we are moving and its position
    piece_on_moving_from_square = game.get_game_piece_at_position(moving_from_square)
    old_position = piece_on_moving_from_square.get_position()

    # Find the general for the team of the piece we are moving, the current general. When checking for check for the
    # opposite team, we set evaluate_for_opposing_general to True
    if evaluate_for_opposing_general:
        current_general = find_opposing_general(game)
    else:
        current_general = find_current_general(game)

    current_general_position = current_general.get_position()

    # Save the piece on the landing square in case there is something there
    piece_at_destination = game.get_game_piece_at_position(moving_to_square)

    # Remove the piece at the old position, set the piece on the new position.
    game.remove_piece(old_position)
    piece_on_moving_from_square.set_position(moving_to_square)
    game.add_piece(piece_on_moving_from_square)

    # See if the generals can see each other; False if they can. True if they can't.
    generals_can_not_see_each_other = can_generals_not_see_each_other(game)

    # Generate the threat dictionary for the board in the updated state.
    new_threat_dictionary = generate_threat_dictionary(game, current_general.get_team())

    # Move the board back
    game.remove_piece(moving_to_square)
    game.add_piece(piece_at_destination)
    piece_on_moving_from_square.set_position(old_position)
    game.add_piece(piece_on_moving_from_square)

    # If the current general's position is found in the new threat dictionary, which contains all the moves possible
    # if the hypothetical move occurred, the move results in check and the appropriate flag is set.
    move_results_in_check = False
    for piece in new_threat_dictionary:
        if current_general_position in new_threat_dictionary[piece]:
            move_results_in_check = True

        # If the piece that moved is a General we have to evaluate both positions, origin and destination to ensure the
        # General escapes check and is not moving into check.
        if game.get_game_piece_at_position(moving_from_square).get_type() == 'General':
            if moving_to_square in new_threat_dictionary[piece]:
                move_results_in_check = True

    # The results of the analysis are returned; False if the move results in check, true otherwise.
    if move_results_in_check:
        return False

    # If the Generals can see each other, return False.
    if not generals_can_not_see_each_other:
        return False

    return True


def find_current_general(game):
    """
    Simple function that searches the board and returns the General object belonging to the team of the current player.
    """
    current_general = None
    board = game.get_game_board()
    for row in board:
        for space in row:
            if space.get_type() == 'General' and space.get_team() == game.get_current_player():
                current_general = space

    return current_general


def find_opposing_general(game):
    """
    Simple function that searches the board and returns the General object belonging to the team of the opposing player.
    """
    opposing_general = None
    board = game.get_game_board()
    for row in board:
        for space in row:
            if space.get_type() == 'General' and space.get_team() != game.get_current_player():
                opposing_general = space

    return opposing_general


def can_generals_not_see_each_other(game):
    """
    Checks to see if the General piece for both players are in the same column/file. If they are, it determines if 
    there is at least one piece (obstruction) intervening between the two Generals.
    """
    # Get the position for each general and then get the indices for each general for comparison.
    opposing_general_position = find_opposing_general(game).get_position()
    current_general_position = find_current_general(game).get_position()
    opposing_general_column, opposing_general_row = algebraic_notation_to_indices(opposing_general_position)
    current_general_column, current_general_row = algebraic_notation_to_indices(current_general_position)

    # If both Generals are in different columns, return true, no need to examine any further.
    if opposing_general_column != current_general_column:
        return True

    # Line of sight is the path between the two General pieces. We only care about the pieces in between the generals.
    line_of_sight = piece_linear_path_helper(current_general_position, opposing_general_position)
    line_of_sight = line_of_sight[1:len(line_of_sight) - 1]

    # If there is at least one GamePiece in the region between the two Generals, there is an obstruction. 
    obstruction = False
    for square in line_of_sight:
        if game.get_game_piece_at_position(square).get_type() is not None:
            obstruction = True

    # If the Generals view is obstructed, we return True.
    return obstruction


class GamePiece:
    """
    Base class for all game pieces. GamePiece also exclusively represents empty spaces on the board. Pieces that
    are not empty spaces are subclassed (derived) from GamePiece. Empty spaces will not be subclassed but 
    self._piece_type will be None.
    """

    def __init__(self, piece_type, team, square):
        """
        Every derivative class needs to know these traits such as what type of piece they are, if they are allowed
        to leave the palace, or if they have crossed the river. Every game piece is created by giving it a piece_type (
        string/given by subclass constructor), a team (string), and a square (string).
        """
        self._piece_type = piece_type  # Assigned by subclass constructor. None for empty spaces.
        self._team = team  # Either 'Red' or 'Black'. Assigned by add_piece().
        self._rules = []  # List of tuples that identify valid moves for a piece. Not all pieces have this.
        self._is_allowed_to_leave_palace = True  # Determines if piece is allowed to leave the palace.
        self._is_allowed_to_cross_river = True  # Determines if the piece is allowed to cross the river.
        self._has_crossed_river = False  # Determines if the piece has crossed the river.
        self._position = square  # Holds the current position for the piece.
        self._has_static_move_set = False  # Determines if the piece will use _rules to determine valid moves.

    def list_possible_moves(self, game):
        """
        Returns a list of possible moves for the piece. The piece requires a XiangqiGame object to have access to
        the board and board methods. This will only be called for rule based pieces such as the Soldier, General and
        Advisor.
        """

        # We start with a list of possible moves, we will also need the current position of the piece, and its indices.
        possible_moves = []
        current_square = self.get_position()
        current_column, current_row = algebraic_notation_to_indices(current_square)

        # Compile a list of valid possible moves for the piece based on the pieces rule set.
        rules = self.get_rules()
        for rule in rules:
            possible_move = indices_to_algebraic_notation(current_column + rule[0], current_row + rule[1])

            # Since the conversion will return False on out of bounds entries, we only add valid moves to the list to
            # start with. This eliminates 'False' from being appended to the list.
            if possible_move:
                possible_moves.append(possible_move)

        # Apply the remaining rules to the piece such as...
        for possible_move in possible_moves:

            # If the piece has to stay in the palace, we enforce that here.
            if not game.get_game_piece_at_position(current_square).is_allowed_to_leave_palace():
                if game.get_game_piece_at_position(current_square).get_team() == 'Black':
                    if possible_move not in BLACK_PALACE:
                        possible_moves.remove(possible_move)
                else:
                    if possible_move not in RED_PALACE:
                        possible_moves.remove(possible_move)

            # Make sure if the piece is not allowed to cross the river, it doesn't.
            if not game.get_game_piece_at_position(current_square).is_allowed_to_cross_river():
                team = game.get_game_piece_at_position(current_square).get_team()
                if team == 'Black':
                    if algebraic_notation_to_indices(possible_move)[1] >= 5:
                        possible_moves.remove(possible_move)
                else:
                    if algebraic_notation_to_indices(possible_move)[1] <= 4:
                        possible_moves.remove(possible_move)

        # Once the possible moves have been generated, we return the list.
        return possible_moves

    def is_valid_move(self, game, moving_from_square, moving_to_square):
        """
        Used to process a piece's ruleset. Depending on the piece, this method may be called in addition to a
        subclass method that overrides this method. This method enforces valid moves by the player. In addition to
        the ruleset, it makes sure the player is not moving out of bounds, or trying to capture its own piece, etc.
        """

        # If the piece has a static move set, run through it to see if the move is valid according to the ruleset.
        if game.get_game_piece_at_position(moving_from_square).has_static_move_set():
            valid_move_according_to_rules = False
            possible_moves = self.list_possible_moves(game)
            if moving_to_square in possible_moves:
                valid_move_according_to_rules = True

            if not valid_move_according_to_rules:
                return False

        # Checking for out-of-bounds rows and columns
        if not algebraic_notation_to_indices(moving_from_square):
            return False
        elif not algebraic_notation_to_indices(moving_to_square):
            return False

        # Make sure player is not trying to capture its own piece.
        if game.get_game_piece_at_position(moving_to_square).get_team() == \
                game.get_game_piece_at_position(moving_from_square).get_team():
            return False

        # Make sure the player is not trying to no-move (to and from are the same space).
        if algebraic_notation_to_indices(moving_from_square) == algebraic_notation_to_indices(moving_to_square):
            return False

        return True

    def move_piece(self, game, moving_from_square, moving_to_square):
        """Updates the self._position value to the new square."""
        self.set_position(moving_to_square)
        game.remove_piece(moving_from_square)
        game.add_piece(self)

    def get_type(self):
        """Returns the piece type."""
        return self._piece_type

    def get_team(self):
        """Returns the team as a string that the piece belongs to."""
        return self._team

    def get_rules(self):
        """
        Returns the list of tuples that denote the valid moves the piece can make. Used for limited movement
        pieces such as the Solider and General. Pieces such as the Cannon do not implement this since the number of
        moves they can make at any point are variable.
        """
        return self._rules

    def set_position(self, square):
        """Sets the position of the piece."""
        self._position = square

    def get_position(self):
        """Gets the position for the piece."""
        return self._position

    def has_static_move_set(self):
        """Gets the boolean value for if the piece has a static moveset."""
        return self._has_static_move_set

    def is_allowed_to_leave_palace(self):
        """Returns a boolean indicating if the piece is allowed to leave it's palace."""
        return self._is_allowed_to_leave_palace

    def is_allowed_to_cross_river(self):
        """Returns a boolean indicating if the piece is allowed to traverse the river."""
        return self._is_allowed_to_cross_river

    def has_crossed_river(self):
        """Returns a boolean indicating if the piece has crossed the river in the current game."""
        return self._has_crossed_river

    def set_crossed_river(self):
        """Sets the _has_crossed_river attribute for the piece to true."""
        self._has_crossed_river = True

    def debug_team_color_string_helper(self, label):
        """Used by debug_print_board() to colorize each cell of the board according to the team of the piece."""
        if self._team == 'Red':
            return '\033[38;5;196m\033[48;5;52m' + label + '\033[0m'
        elif self._team == 'Black':
            return '\033[38;5;0m\033[48;5;15m' + label + '\033[0m'
        else:
            return '\033[48;5;238m' + label + '\033[0m'


class General(GamePiece):
    """General GamePiece. Contains the ruleset, data to aid in debugging and also overrides is_valid_move()."""

    def __init__(self, team, square):
        """General constructor. Has a ruleset and cannot leave the palace."""
        super().__init__('General', team, square)
        self._rules = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self._is_allowed_to_leave_palace = False
        self._has_static_move_set = True

    def __str__(self):
        """Overridden to colorize text."""
        return self.debug_team_color_string_helper('  General  ')

    def is_valid_move(self, game, moving_from_square, moving_to_square):
        """
        Tries to move the General, returns False if that results in check. Determines if the move will result in
        check. Try_move checks to see if there is 'flying general' conflict also, so we don't have to check for that
        here.
        """
        if self.get_team() != game.get_current_player():
            if not try_move(moving_from_square, moving_to_square, game, True):
                return False
            return super().is_valid_move(game, moving_from_square, moving_to_square)
        if not try_move(moving_from_square, moving_to_square, game):
            return False
        return super().is_valid_move(game, moving_from_square, moving_to_square)


class Advisor(GamePiece):
    """Advisor GamePiece."""

    def __init__(self, team, square):
        """Has a ruleset and cannot leave the palace."""
        super().__init__('Advisor', team, square)
        self._rules = [(-1, -1), (1, 1), (-1, 1), (1, -1)]
        self._is_allowed_to_leave_palace = False
        self._has_static_move_set = True

    def __str__(self):
        """Overridden to colorize text."""
        return self.debug_team_color_string_helper('  Advisor  ')


class Elephant(GamePiece):
    """Elephant GamePiece. Contains the ruleset and data to aid in debugging."""

    def __init__(self, team, square):
        """Has a ruleset and cannot cross the river."""
        super().__init__('Elephant', team, square)
        self._rules = [(-2, -2), (2, 2), (2, -2), (-2, 2)]
        self._is_allowed_to_cross_river = False
        self._has_static_move_set = True

    def __str__(self):
        """Overridden to colorize text."""
        return self.debug_team_color_string_helper('  Elephant ')

    def is_valid_move(self, game, moving_from_square, moving_to_square):
        """
        Processes the ruleset for an Elephant GamePiece. The subclass version of the function checks what is being
        referred to as the intermediate space. For example, an elephant at 'c1' moving to 'a3' would have to traverse
        the intermediate space of 'b2'. This overriding function ensures that we are not 'jumping' any pieces. When
        the function is done, we then call the superclass version of the method to check the remaing rules.
        """

        # Check the intermediate space for piece to ensure that no jumps occurred.
        if algebraic_notation_to_indices(moving_to_square)[0] > algebraic_notation_to_indices(moving_from_square)[0]:
            intermediate_column = algebraic_notation_to_indices(moving_from_square)[0] + 1
        else:
            intermediate_column = algebraic_notation_to_indices(moving_from_square)[0] - 1
        if algebraic_notation_to_indices(moving_to_square)[1] > algebraic_notation_to_indices(moving_from_square)[1]:
            intermediate_row = algebraic_notation_to_indices(moving_from_square)[1] + 1
        else:
            intermediate_row = algebraic_notation_to_indices(moving_from_square)[1] - 1
        if game.get_game_piece_at_position(indices_to_algebraic_notation(intermediate_column,
                                                                         intermediate_row)).get_type() is \
                not None:
            return False
        return super().is_valid_move(game, moving_from_square, moving_to_square)


class Chariot(GamePiece):
    """Chariot GamePiece. Contains the ruleset and data to aid in debugging."""

    def __init__(self, team, square):
        """No special variables."""
        super().__init__('Chariot', team, square)

    def __str__(self):
        """Overridden to colorize text."""
        return self.debug_team_color_string_helper('  Chariot  ')

    def is_valid_move(self, game, moving_from_square, moving_to_square):
        """
        The Chariot must first move either vertically or horizontally. We then make sure we aren't jumping any
        pieces. These are the only two rules for the Chariot as it considered one of the most 'free' pieces in the
        game.
        """
        # First we need to ensure vertical or horizontal movement.
        if not is_vertical_or_horizontal_move(moving_from_square, moving_to_square):
            return False

        # Make a list of every square between the Chariot and its destination
        squares_between_chariot_and_target = piece_linear_path_helper(moving_from_square, moving_to_square)

        # Now we check each square in the list for pieces to make sure none are being 'jumped'.
        for square in squares_between_chariot_and_target:
            if square == moving_from_square or square == moving_to_square:
                continue
            elif game.get_game_piece_at_position(square).get_type() is not None:
                return False
        return True

    def list_possible_moves(self, game):
        """
        We override list_possible_moves() since the Chariot does not use a static ruleset. Based on the target square
        the player enters, the possible moves will be different in quantity.
        """

        # We setup a list for possible moves and confirmed moves, get the current position for the piece,
        # duplicate the column and row so they can be used in looping algorithms.
        possible_moves = []
        confirmed_moves = []
        current_square = self.get_position()
        current_column, current_row = algebraic_notation_to_indices(current_square)
        column, row = current_column, current_row
        searching = True  # True while the algorithm is running.
        empty_space = True  # True if the loop detects an empty space, becomes False when another GamePiece is detected.

        # This loop evaluates each direction outward from the Chariot. Each leg of the loop terminates when another
        # GamePiece that is not of type None (empty space) is encountered.
        while searching:

            # Search outward to the right
            column = current_column + 1

            # While we only see empty spaces search...
            while empty_space:

                # If we are still within the bounds of the game board...
                if indices_to_algebraic_notation(column, row):

                    # Get the type of piece on the current space, if None, add it to the list, otherwise add it to
                    # the list and stop searching (since we can't jump pieces).
                    if game.get_game_piece_at_position(indices_to_algebraic_notation(column, row)).get_type() is None:
                        possible_moves.append(indices_to_algebraic_notation(column, row))
                    else:
                        possible_moves.append(indices_to_algebraic_notation(column, row))
                        empty_space = False
                    column += 1
                else:
                    empty_space = False

            # Reset and start searching outward to the left.
            column = current_column - 1
            empty_space = True
            while empty_space:
                if indices_to_algebraic_notation(column, row):
                    if game.get_game_piece_at_position(indices_to_algebraic_notation(column, row)).get_type() is None:
                        possible_moves.append(indices_to_algebraic_notation(column, row))
                    else:
                        possible_moves.append(indices_to_algebraic_notation(column, row))
                        empty_space = False
                    column -= 1
                else:
                    empty_space = False

            # Reset and start searching downward. (Increasing array index.)
            column = current_column
            row = current_row + 1
            empty_space = True
            while empty_space:
                if indices_to_algebraic_notation(column, row):
                    if game.get_game_piece_at_position(indices_to_algebraic_notation(column, row)).get_type() is None:
                        possible_moves.append(indices_to_algebraic_notation(column, row))
                    else:
                        possible_moves.append(indices_to_algebraic_notation(column, row))
                        empty_space = False
                    row += 1
                else:
                    empty_space = False

            # Reset and start searching upward. (Decreasing array index.)
            row = current_row - 1
            empty_space = True
            while empty_space:
                if indices_to_algebraic_notation(column, row):
                    if game.get_game_piece_at_position(indices_to_algebraic_notation(column, row)).get_type() is None:
                        possible_moves.append(indices_to_algebraic_notation(column, row))
                    else:
                        possible_moves.append(indices_to_algebraic_notation(column, row))
                        empty_space = False
                    row -= 1
                else:
                    empty_space = False

            # We are done so we break the outtermost while loop.
            searching = False

        # We examine each move against the superclass method to ensure we aren't breaking any of the general
        # constraints of the game. If they're valid, they are added to confirmed moves, which is returned by this
        # method.
        for move in possible_moves:
            if super().is_valid_move(game, current_square, move):
                confirmed_moves.append(move)

        return confirmed_moves


class Horse(GamePiece):
    """Horse GamePiece. Contains the ruleset and data to aid in debugging."""

    def __init__(self, team, square):
        """Horse has a ruleset."""
        super().__init__('Horse', team, square)
        self._rules = [(-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2)]
        self._has_static_move_set = True

    def __str__(self):
        """Overridden to colorize text."""
        return self.debug_team_color_string_helper('   Horse   ')

    def is_valid_move(self, game, moving_from_square, moving_to_square):
        """
        Processes the ruleset for a Horse GamePiece. This method overrides the superclass method because we must
        check for conditions such as 'hobbling the horses foot'. That is, there can be no obstructing pieces between
        the Horse and its destination (moving_to_square).
        """

        # We get the column and row indices of the origin and destination fo the horse, we also calculate the
        # difference between the values which will give us the direction the piece is travelling.
        column_from = algebraic_notation_to_indices(moving_from_square)[0]
        column_to = algebraic_notation_to_indices(moving_to_square)[0]
        column_delta = column_to - column_from
        row_from = algebraic_notation_to_indices(moving_from_square)[1]
        row_to = algebraic_notation_to_indices(moving_to_square)[1]
        row_delta = row_to - row_from

        # We know that if the piece is moving to the right overall 2 spaces, we have to check one space to the right
        # first. If this space is obstructed, the move is not valid.
        if column_delta == 2:
            # check the same row to the right 1
            intermediate_position = indices_to_algebraic_notation(column_to - 1, row_from)
            if game.get_game_piece_at_position(intermediate_position).get_type() is not None:
                return False

        # If we are moving overall left 2 spaces, check one space to the left.
        elif column_delta == -2:
            # check same row to the left 1
            intermediate_position = indices_to_algebraic_notation(column_to + 1, row_from)
            if game.get_game_piece_at_position(intermediate_position).get_type() is not None:
                return False

        # If we aren't moving horizontally, we are moving vertically.
        else:
            # If we are moving down, we must check down one space.
            if row_delta == 2:
                # check same column down one square
                intermediate_position = indices_to_algebraic_notation(column_from, row_to - 1)
                if game.get_game_piece_at_position(intermediate_position).get_type() is not None:
                    return False

            # The last case is if we are moving up, we check up one space.
            elif row_delta == -2:
                # check same column up one square
                intermediate_position = indices_to_algebraic_notation(column_from, row_to + 1)
                if game.get_game_piece_at_position(intermediate_position).get_type() is not None:
                    return False

        # We then return the superclass method to make sure the origin and destination are valid according to the
        # general rules of the game.
        return super().is_valid_move(game, moving_from_square, moving_to_square)


class Cannon(GamePiece):
    """Cannon GamePiece. Contains the ruleset and data to aid in debugging."""

    def __init__(self, team, square):
        """There are no special data members for Cannon."""
        super().__init__('Cannon', team, square)

    def __str__(self):
        """Overridden to colorize text."""
        return self.debug_team_color_string_helper('  Cannon   ')

    def is_valid_move(self, game, moving_from_square, moving_to_square):
        """Cannons must move in an orthogonal fashion. They must also jump a piece before capturing a piece. """
        # Ensure orthogonal movement.
        if not is_vertical_or_horizontal_move(moving_from_square, moving_to_square):
            return False

        # Generate the path between the cannon and its target
        squares_between_cannon_and_target = piece_linear_path_helper(moving_from_square, moving_to_square)

        # First we establish how many pieces, if any, the Cannon is jumping by making this move.
        jumps = 0
        for square in squares_between_cannon_and_target:
            if square == moving_from_square or square == moving_to_square:
                continue
            elif game.get_game_piece_at_position(square).get_type() is not None:
                jumps += 1

        # If the Cannon didn't jump any pieces, it cannot capture a piece.
        if jumps == 0 and game.get_game_piece_at_position(moving_to_square).get_type() is not None:
            return False

        # If the Cannon jumped a piece but didn't capture a piece, this move is also invalid.
        if jumps == 1 and game.get_game_piece_at_position(moving_to_square).get_type() is None:
            return False

        # The cannon cannot jump more than 1 piece.
        if jumps > 1:
            return False

        return True

    def list_possible_moves(self, game):
        """
        This function returns a list of the possible moves that Cannon can make which could be threatening to another
        piece. It is used when evaluating for check.
        """

        # We establish two lists, possible moves and confirmed moves.  We also get the current position of the piece
        # and the corresponding array (board) indices that go along with it.
        possible_moves = []
        confirmed_moves = []
        current_square = self.get_position()
        current_column, current_row = algebraic_notation_to_indices(current_square)
        column, row = current_column, current_row
        searching = True  # True while the alogrithm is running.

        # Begin searching for possible valid moves
        while searching:

            # Search from origin to the right.
            jumps = 0
            column = current_column + 1

            # We start by searching with jumps = 0.
            while jumps < 2:

                # If the array index is in bounds...
                if indices_to_algebraic_notation(column, row):

                    # If the space as we search is empty...
                    if game.get_game_piece_at_position(indices_to_algebraic_notation(column, row)).get_type() is None:

                        # If we have jumped at least one piece, its a possible attack for the Cannon.
                        if jumps >= 1:
                            possible_moves.append(indices_to_algebraic_notation(column, row))

                    # If the space is occupied, friend of foe...
                    else:

                        # If we haven't jumped a piece yet, we increase the jump count.
                        if jumps < 1:
                            jumps += 1

                        # If we jumped a piece, we can land on the next encountered piece.
                        else:
                            possible_moves.append(indices_to_algebraic_notation(column, row))
                            jumps += 1
                    column += 1

                # If we leave the edge of the game board, we break.
                else:
                    break

            # Reset flags and search from origin to the left, same method.
            jumps = 0
            column = current_column - 1
            while jumps < 2:
                if indices_to_algebraic_notation(column, row):
                    if game.get_game_piece_at_position(indices_to_algebraic_notation(column, row)).get_type() is None:
                        if jumps >= 1:
                            possible_moves.append(indices_to_algebraic_notation(column, row))
                    else:
                        if jumps < 1:
                            jumps += 1
                        else:
                            possible_moves.append(indices_to_algebraic_notation(column, row))
                            jumps += 1
                    column -= 1
                else:
                    break

            # Reset flags and search from origin, down (numerically increasing array index).
            jumps = 0
            column = current_column
            row = current_row + 1
            while jumps < 2:
                if indices_to_algebraic_notation(column, row):
                    if game.get_game_piece_at_position(indices_to_algebraic_notation(column, row)).get_type() is None:
                        if jumps >= 1:
                            possible_moves.append(indices_to_algebraic_notation(column, row))
                    else:
                        if jumps < 1:
                            jumps += 1
                        else:
                            possible_moves.append(indices_to_algebraic_notation(column, row))
                            jumps += 1
                    row += 1
                else:
                    break

            # Reset flags and search from origin, up (numerically decreasing array index).
            jumps = 0
            row = current_row - 1
            while jumps < 2:
                if indices_to_algebraic_notation(column, row):
                    if game.get_game_piece_at_position(indices_to_algebraic_notation(column, row)).get_type() is None:
                        if jumps >= 1:
                            possible_moves.append(indices_to_algebraic_notation(column, row))
                    else:
                        if jumps < 1:
                            jumps += 1
                        else:
                            possible_moves.append(indices_to_algebraic_notation(column, row))
                            jumps += 1
                    row -= 1
                else:
                    break

            # When we are done, we clear the searching flag to break the outtermost while loop.
            searching = False

        # We reconcile all the moves we found with the general rules of the game. All the ones deemed valid are
        # appended to confirmed moves which is then returned by this function.
        for move in possible_moves:
            if super().is_valid_move(game, current_square, move):
                confirmed_moves.append(move)

        return confirmed_moves


class Soldier(GamePiece):
    """Soldier GamePiece. Contains the ruleset and data to aid in debugging."""

    def __init__(self, team, square):
        """Soldiers have static rulesets for moving"""
        super().__init__('Soldier', team, square)
        self._rules = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        self._has_static_move_set = True

    def __str__(self):
        """Overridden to colorize text."""
        return self.debug_team_color_string_helper('  Soldier  ')

    def is_valid_move(self, game, moving_from_square, moving_to_square):
        """Processes the ruleset for a Solider GamePiece."""
        # Enforce vertical moves if the soldier has not crossed the river. If they have, enforce horizontal or
        # vertical moves.
        if not game.get_game_piece_at_position(moving_from_square).has_crossed_river():
            if not is_vertical_move(moving_from_square, moving_to_square):
                return False
        else:
            if not is_vertical_move(moving_from_square, moving_to_square):
                if not is_horizontal_move(moving_from_square, moving_to_square):
                    return False

        # Enforce not moving backwards.
        if is_backwards_move(moving_from_square, moving_to_square, game.get_game_piece_at_position(
                moving_from_square).get_team()):
            return False

        # See if the solider crossed the river and set the flag for that piece accordingly then return True.
        team = game.get_game_piece_at_position(moving_from_square).get_team()
        if team == 'Black':
            if algebraic_notation_to_indices(moving_to_square)[1] >= 5:
                game.get_game_piece_at_position(moving_from_square).set_crossed_river()
        else:
            if algebraic_notation_to_indices(moving_to_square)[1] <= 4:
                game.get_game_piece_at_position(moving_from_square).set_crossed_river()

        # Run the superclass version of this method to ensure the requested move is valid according to the general
        # rules of the game.
        return super().is_valid_move(game, moving_from_square, moving_to_square)


class XiangqiGame:
    """Base class for the entire module/game. Contains things like the game board and game state."""

    def __init__(self):
        """XiangqiGame constructor. Sets the state to UNFINISHED, builds and sets the board."""
        self._game_state = 'UNFINISHED'  # Gamestate always starts at unfinished.

        # The gameboard is an array of 10 rows, columns wide. There are 90 squares total.
        self._game_board = [[GamePiece(None, None, indices_to_algebraic_notation(column, row)) for column in range(9)]
                            for row in range(10)]

        self.new_game()  # When a game object is created, the board is set.
        self._current_player = 'Red'  # By the rules of the game, Red goes first.
        self._red_is_in_check = False  # True when Red is in check.
        self._black_is_in_check = False  # True when Black is in check.

    def new_game(self):
        """Routine to clear the board then add all 32 pieces (16 per player) to the board."""

        # Clear the board first.
        self.set_game_board([[GamePiece(None, None, indices_to_algebraic_notation(column, row)) for column in range(9)]
                            for row in range(10)])

        # Add all the pieces.
        self.add_piece(General('Red', 'e1'))
        self.add_piece(Advisor('Red', 'd1'))
        self.add_piece(Advisor('Red', 'f1'))
        self.add_piece(Elephant('Red', 'c1'))
        self.add_piece(Elephant('Red', 'g1'))
        self.add_piece(Horse('Red', 'b1'))
        self.add_piece(Horse('Red', 'h1'))
        self.add_piece(Chariot('Red', 'a1'))
        self.add_piece(Chariot('Red', 'i1'))
        self.add_piece(Cannon('Red', 'b3'))
        self.add_piece(Cannon('Red', 'h3'))
        self.add_piece(Soldier('Red', 'a4'))
        self.add_piece(Soldier('Red', 'c4'))
        self.add_piece(Soldier('Red', 'e4'))
        self.add_piece(Soldier('Red', 'g4'))
        self.add_piece(Soldier('Red', 'i4'))

        self.add_piece(General('Black', 'e10'))
        self.add_piece(Advisor('Black', 'd10'))
        self.add_piece(Advisor('Black', 'f10'))
        self.add_piece(Elephant('Black', 'c10'))
        self.add_piece(Elephant('Black', 'g10'))
        self.add_piece(Horse('Black', 'b10'))
        self.add_piece(Horse('Black', 'h10'))
        self.add_piece(Chariot('Black', 'a10'))
        self.add_piece(Chariot('Black', 'i10'))
        self.add_piece(Cannon('Black', 'b8'))
        self.add_piece(Cannon('Black', 'h8'))
        self.add_piece(Soldier('Black', 'a7'))
        self.add_piece(Soldier('Black', 'c7'))
        self.add_piece(Soldier('Black', 'e7'))
        self.add_piece(Soldier('Black', 'g7'))
        self.add_piece(Soldier('Black', 'i7'))

    def next_player_turn(self):
        """Advances the current player to the next player."""
        if self._current_player == 'Red':
            self._current_player = 'Black'
        else:
            self._current_player = 'Red'

    def get_current_player(self):
        """Returns the current player."""
        return self._current_player

    def get_defending_player(self):
        """Gets the defending player."""
        if self.get_current_player() == 'Red':
            return 'Black'
        else:
            return 'Red'

    def get_game_state(self):
        """Returns the current game state."""
        return self._game_state

    def get_game_piece_at_position(self, square):
        """Returns the GamePiece object at the position (square) provided."""
        column, row = algebraic_notation_to_indices(square)
        return self.get_game_board()[row][column]

    def add_piece(self, piece):
        """Adds a GamePiece object at the position (square) provided."""
        column, row = algebraic_notation_to_indices(piece.get_position())
        self.get_game_board()[row][column] = piece

    def set_player_in_check(self, player):
        """Sets player in check flag according to the color the team the player belongs to."""
        if player == 'Red':
            self._red_is_in_check = True
        elif player == 'Black':
            self._black_is_in_check = True

    def set_player_not_in_check(self, player):
        """Clears the player in check flag for the color of the team that the passed in 'player' belongs to."""
        if player == 'Red':
            self._red_is_in_check = False
        elif player == 'Black':
            self._black_is_in_check = False

    def get_player_in_check(self, player):
        """Gets the player in check flag for the correct team based on the player passed into the function."""
        if player == 'Red':
            return self._red_is_in_check
        elif player == 'Black':
            return self._black_is_in_check

    def remove_piece(self, square):
        """Sets the cell at the position (square) provided to GamePiece(None, None) aka an 'empty' space."""
        column, row = algebraic_notation_to_indices(square)
        self.get_game_board()[row][column] = GamePiece(None, None, square)

    def get_game_board(self):
        """Returns the game board."""
        return self._game_board

    def set_game_board(self, board):
        """Sets the game board."""
        self._game_board = board

    def clear_game_board(self):
        self.set_game_board([[GamePiece(None, None, indices_to_algebraic_notation(column, row)) for column in range(9)]
                            for row in range(10)])

    def set_game_state(self, state):
        """Sets the gamestate to one of three predefined states."""
        if state == 'UNFINISHED' or state == 'RED_WON' or state == 'BLACK_WON':
            self._game_state = state

    def is_in_check(self, player):
        """Returns true if the passed parameter player is in check, otherwise returns false."""
        # Player is converted to title case then checked for validity. Player must be either 'Black' or 'Red'.
        player = player.title()
        if player != 'Black' and player != 'Red':
            return False

        # Get all available moves for the 'defending' player and the current board.
        threat_dictionary = generate_threat_dictionary(self, player)
        board = self.get_game_board()

        # Get all the available moves and current position for the passed in player's general.
        # When the player on the opposite team is passed in as an argument, we set evaluate_for_opposing_general
        # to True
        if player == self.get_current_player():
            general = find_current_general(self)
            evaluate_for_opposing_general = False
        else:
            general = find_opposing_general(self)
            evaluate_for_opposing_general = True

        general_position = general.get_position()
        general_possible_moves = general.list_possible_moves(self)

        # If the general is being threatened with capture, we set the appropriate check condition.
        for piece in threat_dictionary:
            if general_position in threat_dictionary[piece]:
                self.set_player_in_check(player)
                break
            else:
                self.set_player_not_in_check(player)

        # Eliminate possible moves that break the rules of the game or individual pieces.
        invalid_moves = []
        for possible_move in general_possible_moves:
            if not general.is_valid_move(self, general_position, possible_move):
                if possible_move not in invalid_moves:
                    invalid_moves.append(possible_move)

        # Try the remaining moves to see if they will get the general out of check.
        for possible_move in general_possible_moves:
            if not try_move(general_position, possible_move, self, evaluate_for_opposing_general):
                if possible_move not in invalid_moves:
                    invalid_moves.append(possible_move)

        # Remove all the invalid moves from the general's possible moves.
        for invalid_move in invalid_moves:
            general_possible_moves.remove(invalid_move)

        # If the general can be captured and has no available moves, the game is won and checkmate is set.
        player_checkmate = False
        if len(general_possible_moves) == 0:
            if self.verify_checkmate(evaluate_for_opposing_general):
                player_checkmate = True

        # If there is checkmate, we set the appropriate gamestate.
        if player_checkmate:
            if player == 'Red':
                self.set_game_state('BLACK_WON')
            else:
                self.set_game_state('RED_WON')

        # Return the appropriate boolean value for the correct player depending on if they are in check.
        return self.get_player_in_check(player)

    def verify_checkmate(self,evaluate_for_opposing_general=False):
        """
        Verifies that after trying every possible intervening move, there is no way to prevent checkmate. When
        evaluate for opposing general is True, will evaluate checkmate for the opposing team.
        """

        # Gets the appropriate intervention dictionary.
        if evaluate_for_opposing_general:
            possible_intervention_dictionary = generate_threat_dictionary(self, self.get_current_player())
        else:
            possible_intervention_dictionary = generate_threat_dictionary(self, self.get_defending_player())

        # Evaluates all possible moves to see if a move exists that does not result in check.
        checkmate = True
        for piece in possible_intervention_dictionary:
            for move in possible_intervention_dictionary[piece]:
                if try_move(piece.get_position(), move, self, evaluate_for_opposing_general):
                    checkmate = False

        return checkmate

    def make_move(self, moving_from_square, moving_to_square):
        """Moves piece from one square to another square if doing so adheres to all the rules defined for the game."""

        # Verify the user didn't enter bad squares.
        if not algebraic_notation_to_indices(moving_from_square) or not algebraic_notation_to_indices(moving_to_square):
            return False

        # Verify the game state is unfinished.
        if self.get_game_state() != 'UNFINISHED':
            return False

        # Verify the correct player is taking a turn.
        if self.get_game_piece_at_position(moving_from_square).get_team() != self.get_current_player():
            return False

        # Check to see if it is a valid move for the piece.
        if not self.get_game_piece_at_position(moving_from_square).is_valid_move(self, moving_from_square,
                                                                                 moving_to_square):
            return False

        # Try the move and see if it causes check.. TRY MOVE THING
        if not try_move(moving_from_square, moving_to_square, self):
            return False

        # If all conditions to make the move in a valid manner are satisfied, then make the move.
        self.get_game_piece_at_position(moving_from_square).move_piece(self, moving_from_square, moving_to_square)

        # Update the check status for both sides.
        self.is_in_check(self.get_current_player())
        self.is_in_check(self.get_defending_player())

        # Advance to the next players turn
        self.next_player_turn()
        return True
