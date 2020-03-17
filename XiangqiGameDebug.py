# Author: George Kochera
# Date: 3/11/2020
# Description: Portfolio Project - XiangqiGame_Garbage.py

# All debugging related functions and classes written to aid in debugging XiangqiGame.

from XiangqiGame import XiangqiGame, indices_to_algebraic_notation, generate_threat_dictionary, find_current_general, try_move


class XiangqiGameDebug(XiangqiGame):
    def debug_display_piece(self, square):

        piece = self.get_game_piece_at_position(square)

        print('\nType: {}, Team: {:5}'.format(piece.get_type(), piece.get_team()),
              '| Position according to Piece: {:3}'.format(piece.get_position())
              , end='')

    def debug_display_all_pieces(self):
        print('--- DISPLAY PIECE STATISTICS ROUTINE ---')
        board = self.get_game_board()
        row_index = 0
        for row in board:
            column_index = 0
            for column in row:
                if column.get_type() is not None:
                    self.debug_display_piece(indices_to_algebraic_notation(column_index, row_index))
                    print(' - Position according to Game: {}'.format(
                        indices_to_algebraic_notation(column_index, row_index)), end='')
                column_index += 1
            row_index += 1
        print('\n\n--- END DISPLAY PIECE STATISTICS ROUTINE ---')

    def debug_print_board(self):
        """Prints a text-graphic representation of the game board and pieces."""
        rank = 10
        padding = '   '
        player = self.get_current_player()
        for row in self.get_game_board():
            if rank < 10:
                print(str(rank) + (' ' * 4), end='')
            else:
                print(str(rank) + (' ' * 3), end='')
            for column in row:
                if column.get_type() is None:
                    print(column.debug_team_color_string_helper('[         ]') + padding, end='')
                else:
                    print(str(column) + '   ', end='')
            if rank > 1:
                print('\n' * 2)
            rank -= 1
        file_label = ['     A     ', '     B     ', '     C     ', '     D     ',
                      '     E     ', '     F     ', '     G     ', '     H     ',
                      '     I     ']
        print('\n')
        print(' ' * 5, end='')
        for item in file_label:
            print(item + padding, end='')
        print('\n')
        print('Current turn is: {}'.format(self.get_current_player()))
        print('Black in check: {} | Red in check: {}'.format(self.is_in_check('Black'),
                                                             self.is_in_check('Red')))
        print('\nGame state: {}'.format(self.get_game_state()))
        # self.debug_display_all_pieces()

    def debug_show_all_available_moves(self):
        current_player = self.get_current_player()
        threat_dictionary = generate_threat_dictionary(self, current_player)
        current_general = find_current_general(self)
        general_position = current_general.get_position()
        general_possible_moves = current_general.list_possible_moves(self)

        invalid_moves = []
        for possible_move in general_possible_moves:
            if not current_general.is_valid_move(self, general_position, possible_move):
                if possible_move not in invalid_moves:
                    invalid_moves.append(possible_move)

        for possible_move in general_possible_moves:
            if not try_move(general_position, possible_move, self):
                if possible_move not in invalid_moves:
                    invalid_moves.append(possible_move)

        for invalid_move in invalid_moves:
            general_possible_moves.remove(invalid_move)

        for threat in threat_dictionary:
            print(threat, 'at', threat.get_position(), '--->', threat_dictionary[threat])
        print("Defending general current position: {} | Valid moves: {}".format(general_position,
                                                                                general_possible_moves))

