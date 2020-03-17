# Author: George Kochera
# Date: 3/12/2020
# Description: Portfolio Project (Unit Test Suite) - XiangqiGame_Test.py

# Unittests written to verify that functionality of the game continues to work as development progress was made.
# There are a total of 34 tests that I created to test a variety of mechanics for the game as well as individual pieces.

import unittest
from XiangqiGame import XiangqiGame, GamePiece, General, Advisor, Elephant, Horse
from XiangqiGame import Cannon, Chariot, Soldier


class GeneralTest(unittest.TestCase):
    """Test routines for General GamePiece mechanics."""

    def setUp(self) -> None:
        self.game = XiangqiGame()
        self.game.new_game()

    def test_verify_red_general_cannot_leave_palace(self):
        self.assertTrue(self.game.make_move('e1', 'e2'))
        self.assertTrue(self.game.make_move('e10', 'e9'))
        self.assertTrue(self.game.make_move('e2', 'e3'))
        self.assertTrue(self.game.make_move('e9', 'e8'))
        self.assertFalse(self.game.make_move('e3', 'e4'))

    def test_verify_red_general_can_move_within_palace(self):
        self.assertTrue(self.game.make_move('e1', 'e2'))

    def test_verify_black_general_cannot_leave_palace(self):
        self.assertTrue(self.game.make_move('e1', 'e2'))
        self.assertTrue(self.game.make_move('e10', 'e9'))
        self.assertTrue(self.game.make_move('e2', 'e3'))
        self.assertTrue(self.game.make_move('e9', 'e8'))
        self.assertTrue(self.game.make_move('e3', 'e2'))
        self.assertFalse(self.game.make_move('e8', 'e7'))

    def test_verify_black_general_can_move_within_palace(self):
        self.assertTrue(self.game.make_move('e1', 'e2'))
        self.assertTrue(self.game.make_move('e10', 'e9'))

    def test_moving_red_general_vacates_old_space(self):
        self.game.make_move('e1', 'e2')
        self.assertIsNone(self.game.get_game_piece_at_position('e1').get_type())


class AdvisorTest(unittest.TestCase):
    """Test routines for Advisor GamePiece mechanics."""

    def setUp(self) -> None:
        self.game = XiangqiGame()
        self.game.new_game()

    def test_verify_red_advisor_can_move_diagonally_within_palace(self):
        self.assertTrue(self.game.make_move('d1', 'e2'))

    def test_verify_red_advisor_cannot_move_horizontally(self):
        self.assertFalse(self.game.make_move('d1', 'e1'))

    def test_verify_red_advisor_cannot_leave_palace(self):
        self.assertFalse(self.game.make_move('d1', 'c2'))

    def test_verify_black_advisor_can_move_diagonally_within_palace(self):
        self.assertTrue(self.game.make_move('d1', 'e2'))
        self.assertTrue(self.game.make_move('d10', 'e9'))

    def test_verify_black_advisor_cannot_move_horizontally(self):
        self.assertFalse(self.game.make_move('d10', 'e10'))

    def test_verify_black_advisor_cannot_leave_palace(self):
        self.assertFalse(self.game.make_move('d10', 'c9'))


class HorseTest(unittest.TestCase):
    def setUp(self) -> None:
        self.game = XiangqiGame()
        self.game.new_game()

    def test_both_teams_horses_can_move_legally(self):
        self.assertTrue(self.game.make_move('h1', 'g3'))
        self.assertTrue(self.game.make_move('b10', 'c8'))
        self.assertTrue(self.game.make_move('b1', 'a3'))
        self.assertTrue(self.game.make_move('h10', 'g8'))

    def test_red_horse_cant_move_when_path_is_obstructed_by_own_piece(self):
        self.assertTrue(self.game.make_move('h1', 'g3'))
        self.assertTrue(self.game.make_move('g7', 'g6'))
        self.assertFalse(self.game.make_move('g3', 'f5'))

    def test_black_horse_cant_move_when_path_is_obstructed_by_own_piece(self):
        self.assertTrue(self.game.make_move('c4', 'c5'))
        self.assertTrue(self.game.make_move('h10', 'g8'))
        self.assertTrue(self.game.make_move('e4', 'e5'))
        self.assertFalse(self.game.make_move('g8', 'f6'))


class ElephantTest(unittest.TestCase):
    """Test routines for Elephant GamePiece mechanics."""

    def setUp(self) -> None:
        self.game = XiangqiGame()
        self.game.new_game()

    def test_verify_red_elephant_cannot_jump_piece(self):
        self.game.make_move('e1', 'e2')
        self.game.make_move('e10', 'e9')
        self.game.make_move('e2', 'f2')
        self.game.make_move('e9', 'e8')
        self.assertFalse(self.game.make_move('g1', 'e3'))

    def test_black_elephant_cannot_jump_piece(self):
        self.assertTrue(self.game.make_move('e4', 'e5'))
        self.assertTrue(self.game.make_move('e7', 'e6'))
        self.assertTrue(self.game.make_move('e5', 'e6'))
        self.assertTrue(self.game.make_move('a7', 'a6'))
        self.assertTrue(self.game.make_move('c1', 'e3'))
        self.assertTrue(self.game.make_move('b10', 'a8'))
        self.assertTrue(self.game.make_move('e6', 'f6'))
        self.assertTrue(self.game.make_move('a6', 'a5'))
        self.assertTrue(self.game.make_move('f6', 'f7'))
        self.assertTrue(self.game.make_move('i7', 'i6'))
        self.assertTrue(self.game.make_move('f7', 'f8'))
        self.assertTrue(self.game.make_move('g7', 'g6'))
        self.assertTrue(self.game.make_move('f8', 'f9'))
        self.assertFalse(self.game.make_move('g10', 'e8'))

    def test_black_elephant_cannot_cross_river(self):
        self.game.make_move('g10', 'e8')
        self.game.make_move('e8', 'g6')
        self.game.make_move('i4', 'i5')
        self.assertFalse(self.game.make_move('g6', 'i4'))


class SoldierTest(unittest.TestCase):
    """Test routines for Soldier GamePiece mechanics."""

    def setUp(self) -> None:
        self.game = XiangqiGame()
        self.game.new_game()

    def test_red_soldier_cannot_move_backward(self):
        self.assertFalse(self.game.make_move('g4', 'g3'))

    def test_red_soldier_cannot_move_horizontally_until_river_is_crossed(self):
        self.assertFalse(self.game.make_move('c4', 'd4'))

    def test_red_soldier_can_move_horizontally_once_river_is_crossed(self):
        self.assertTrue(self.game.make_move('e4', 'e5'))
        self.assertTrue(self.game.make_move('g7', 'g6'))
        self.assertTrue(self.game.make_move('e5', 'e6'))
        self.assertTrue(self.game.make_move('g6', 'g5'))
        self.assertTrue(self.game.make_move('e6', 'f6'))
        self.assertTrue(self.game.make_move('g5', 'h5'))

    def test_black_soldier_cannot_move_backward(self):
        self.assertFalse(self.game.make_move('c7', 'c8'))

    def test_black_soldier_cannot_move_horizontally_until_river_is_crossed(self):
        self.assertFalse(self.game.make_move('c4', 'd4'))

    def test_black_soldier_can_move_horizontally_once_river_is_crossed(self):
        self.assertTrue(self.game.make_move('e4', 'e5'))
        self.assertTrue(self.game.make_move('g7', 'g6'))
        self.assertTrue(self.game.make_move('e5', 'e6'))
        self.assertTrue(self.game.make_move('g6', 'g5'))
        self.assertTrue(self.game.make_move('e6', 'f6'))


class CannonTest(unittest.TestCase):
    """Test routines for Cannon GamePiece mechanics."""

    def setUp(self) -> None:
        self.game = XiangqiGame()
        self.game.new_game()

    def test_red_cannon_cannot_jump_more_than_one_piece(self):
        self.game.make_move('a4', 'a5')
        self.game.make_move('a5', 'a6')
        self.game.make_move('a6', 'b6')
        self.assertFalse(self.game.make_move('b3', 'b10'))

    def test_red_cannon_can_capture_piece_after_jump(self):
        self.assertTrue(self.game.make_move('a4', 'a5'))
        self.assertTrue(self.game.make_move('e7', 'e6'))
        self.assertTrue(self.game.make_move('a5', 'a6'))
        self.assertTrue(self.game.make_move('i7', 'i6'))
        self.assertTrue(self.game.make_move('a6', 'b6'))
        self.assertTrue(self.game.make_move('c7', 'c6'))
        self.assertTrue(self.game.make_move('b3', 'b8'))

    def test_black_cannon_cannot_jump_more_than_one_piece(self):
        self.assertTrue(self.game.make_move('a4', 'a5'))
        self.assertTrue(self.game.make_move('h10', 'g8'))
        self.assertTrue(self.game.make_move('a5', 'a6'))
        self.assertTrue(self.game.make_move('g8', 'h10'))
        self.assertTrue(self.game.make_move('a6', 'b6'))
        self.assertFalse(self.game.make_move('b8', 'b1'))

    def test_black_cannon_can_capture_piece_after_jump(self):
        self.assertTrue(self.game.make_move('a4', 'a5'))
        self.assertTrue(self.game.make_move('e7', 'e6'))
        self.assertTrue(self.game.make_move('a5', 'a6'))
        self.assertTrue(self.game.make_move('i7', 'i6'))
        self.assertTrue(self.game.make_move('a6', 'b6'))
        self.assertTrue(self.game.make_move('c7', 'c6'))
        self.assertTrue(self.game.make_move('b3', 'b8'))
        self.assertTrue(self.game.make_move('i6', 'i5'))
        self.assertTrue(self.game.make_move('b6', 'a6'))
        self.assertTrue(self.game.make_move('i5', 'h5'))
        self.assertTrue(self.game.make_move('c4', 'c5'))
        self.assertTrue(self.game.make_move('h8', 'h3'))


class ChariotTest(unittest.TestCase):
    """Test routines for Chariot GamePiece mechanics."""

    def setUp(self) -> None:
        self.game = XiangqiGame()
        self.game.new_game()

    def test_chariot_can_move_in_all_directions(self):
        self.assertTrue(self.game.make_move('a1', 'a3'))
        self.assertTrue(self.game.make_move('a10', 'a9'))
        self.assertTrue(self.game.make_move('i1', 'i2'))
        self.assertTrue(self.game.make_move('i10', 'i8'))
        self.assertTrue(self.game.make_move('b3', 'b10'))
        self.assertTrue(self.game.make_move('a9', 'h9'))
        self.assertTrue(self.game.make_move('a3', 'a2'))

    def test_chariot_can_capture_piece(self):
        self.assertTrue(self.game.make_move('a1', 'a3'))
        self.assertTrue(self.game.make_move('a7', 'a6'))
        self.assertTrue(self.game.make_move('a4', 'a5'))
        self.assertTrue(self.game.make_move('a6', 'a5'))
        self.assertTrue(self.game.make_move('a3', 'a5'))


class GameMechanicsTest(unittest.TestCase):
    """Test routines for overall XiangqiGame mechanics."""

    def setUp(self) -> None:
        self.game = XiangqiGame()
        self.game.new_game()

    def test_board_is_90_squares_total(self):
        board = self.game.get_game_board()
        index = 0
        for row in board:
            for element in row:
                index += 1
        self.assertEqual(90, index)

    def test_black_check_scenario_using_chariot(self):
        self.game.clear_game_board()
        self.game.add_piece(General('Red', 'e1'))
        self.game.add_piece(General('Black', 'e10'))
        self.game.add_piece(Chariot('Red', 'a1'))
        self.game.add_piece(Horse('Red', 'h1'))
        self.game.add_piece(Soldier('Black', 'e7'))
        self.game.make_move('a1', 'a10')
        self.assertTrue(self.game.is_in_check('Black'))
        self.assertFalse(self.game.is_in_check('Red'))

    def test_red_check_scenario_using_chariot(self):
        self.game.clear_game_board()
        self.game.add_piece(General('Red', 'e1'))
        self.game.add_piece(General('Black', 'e10'))
        self.game.add_piece(Chariot('Black', 'a10'))
        self.game.add_piece(Horse('Red', 'h1'))
        self.game.add_piece(Soldier('Black', 'e7'))
        self.game.make_move('h1', 'g3')
        self.game.make_move('a10', 'a1')
        self.assertTrue(self.game.is_in_check('Red'))
        self.assertFalse(self.game.is_in_check('Black'))

    def test_black_checkmate_scenario(self):
        self.game.clear_game_board()
        self.game.add_piece(General('Red', 'e1'))
        self.game.add_piece(General('Black', 'e10'))
        self.game.add_piece(Chariot('Red', 'a1'))
        self.game.add_piece(Chariot('Red', 'i1'))
        self.game.add_piece(Horse('Red', 'h1'))
        self.game.add_piece(Soldier('Black', 'e7'))
        self.game.make_move('a1', 'a9')
        self.game.make_move('e7', 'e6')
        self.game.make_move('i1', 'i10')
        self.assertEqual(self.game.get_game_state(), 'RED_WON')

    def test_red_checkmate_scenario(self):
        self.game.clear_game_board()
        self.game.add_piece(General('Red', 'e1'))
        self.game.add_piece(General('Black', 'e10'))
        self.game.add_piece(Chariot('Black', 'a10'))
        self.game.add_piece(Chariot('Black', 'i10'))
        self.game.add_piece(Horse('Red', 'h1'))
        self.game.add_piece(Soldier('Red', 'e4'))
        self.game.make_move('e1', 'd1')
        self.game.make_move('a10', 'a2')
        self.game.make_move('h1', 'g3')
        self.game.make_move('i10', 'i9')
        self.game.make_move('g3', 'f5')
        self.game.make_move('i9', 'i1')
        self.assertEqual(self.game.get_current_player(), 'Red')
        self.assertEqual(self.game.get_game_state(), 'BLACK_WON')


class InstructorTest(unittest.TestCase):
    def test_readme_code(self):
        game = XiangqiGame()
        move_result = game.make_move('c1', 'e3')
        self.assertTrue(move_result)
        black_in_check = game.is_in_check('black')
        self.assertFalse(black_in_check)
        game.make_move('e7', 'e6')
        state = game.get_game_state()
        self.assertEqual(state, 'UNFINISHED')
