# Author: George Kochera
# Date: 3/12/2020
# Description: Portfolio Project - XiangqiGame_Garbage.py

# File used as 'breadboard' for testing XiangqiGame.

from XiangqiGame import XiangqiGame, GamePiece, General, Advisor, Elephant, Horse
from XiangqiGame import Cannon, Chariot, Soldier
from XiangqiGameDebug import XiangqiGameDebug

# Load the game and display the board.
testgame = XiangqiGameDebug()
testgame.debug_print_board()
testgame.debug_show_all_available_moves()

# testgame.clear_game_board()
# testgame.add_piece(General('Red', 'e1'))
# testgame.add_piece(General('Black', 'e10'))
# testgame.add_piece(Chariot('Black', 'a10'))
# testgame.add_piece(Chariot('Black', 'i10'))
# testgame.add_piece(Horse('Red', 'h1'))
# testgame.add_piece(Soldier('Red', 'e4'))
# testgame.make_move('e1', 'd1')
# testgame.make_move('a10', 'a2')
# testgame.make_move('h1', 'g3')
# testgame.make_move('i10', 'i9')
# testgame.make_move('g3', 'f5')
# testgame.make_move('i9', 'i2')

# testgame.make_move('a1','a2')
# testgame.make_move('a10','a9')
#
# testgame.make_move('a2','d2')
# testgame.make_move('a9','a10')
#
# testgame.make_move('d2','d7')
# testgame.make_move('a10','a9')
#
# testgame.make_move('d7','e7')
# testgame.make_move('d10','e9')
#
# testgame.make_move('b3','b10')


testgame.debug_print_board()
testgame.debug_show_all_available_moves()


# testgame.make_move('a1', 'a2')
# testgame.make_move('a7', 'a6')
#
# testgame.make_move('a2', 'd2')
# testgame.make_move('a6', 'a5')
#
# testgame.make_move('d2', 'd7')
# testgame.make_move('i7', 'i6')
#
# testgame.make_move('d7', 'e7')
# print(testgame.is_in_check('Black'))

# testgame.make_move('c1', 'e3')
# print(testgame.is_in_check('Red'))
# testgame.make_move('b8', 'b1')
# print(testgame.is_in_check('Red'))
# testgame.debug_print_board()

# testgame.debug_print_board()

# Add a piece (must remove new_game() from XiangqiGame() constructor)
# testgame.add_piece(General('Black', 'e10'))

# Make a move
# testgame.make_move('c1','c10')

# Get the game state
# print(testgame.get_game_state())

# See if a player is in check
# print(testgame.is_in_check('black'))

# Sample Game Loop
# while testgame.get_game_state() != 'RED_WON' or testgame.get_game_state() != 'BLACK_WON':
#     square_from = input('Move piece from: ')
#     square_to = input('Move piece to: ')
#     testgame.make_move(square_from,square_to)
#     testgame.debug_print_board()
#     testgame.debug_show_all_available_moves()
#
#     if testgame.get_game_state() == 'RED_WON':
#         print('Red has won the game!')
#         break
#     elif testgame.get_game_state() == 'BLACK_WON':
#         print('Black has won the game!')
#         break

# Readme specified usage
# game = XiangqiGame()
# move_result = game.make_move('c1', 'e3')
# black_in_check = game.is_in_check('black')
# game.make_move('e7', 'e6')
# state = game.get_game_state()
# print(state)

# --------------- SCRATCH CODE FOR DEBUGGING ----------------------
# testgame.add_piece(General('Black', 'e10'))
# testgame.add_piece(General('Red', 'd1'))
# testgame.add_piece(Soldier('Black', 'g9'))
# testgame.add_piece(Soldier('Black', 'd9'))
# testgame.add_piece(Elephant('Black', 'f10'))
# testgame.make_move('d1','d2')
# testgame.make_move('e10','f10')
# testgame.make_move('e1','f1')
# testgame.make_move('f10','h8')
#
#
#
# testgame.debug_print_board()