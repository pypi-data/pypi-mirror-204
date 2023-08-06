import pytest
from unittest.mock import Mock

from ..tic_tac_toe import Game, Board, Player


@pytest.fixture
def board():
    return Board()


@pytest.fixture
def alice():
    return Player('Alice', 'X')


@pytest.fixture
def bob():
    return Player('Bob', 'O')


def test_game_initialization(board, alice, bob):
    game = Game(board=board, player1=alice, player2=bob)

    assert game.board == board
    assert game.player1 == alice
    assert game.player2 == bob


def test_game_alice_wins(board, capsys):
    alice_mock = Mock(spec=Player)
    bob_mock = Mock(spec=Player)

    alice_mock.name = 'Alice'
    alice_mock.piece = 'X'

    bob_mock.name = 'Bob'
    bob_mock.piece = 'O'

    game = Game(board=board, player1=alice_mock, player2=bob_mock)

    alice_mock.get_move.side_effect = [[0, 0], [0, 1], [0, 2]]
    bob_mock.get_move.side_effect = [[1, 0], [1, 1], [1, 2]]

    game.start()

    captured = capsys.readouterr()

    assert 'Alice wins!' in captured.out


def test_game_cats_game(board, capsys):
    alice_mock = Mock(spec=Player)
    bob_mock = Mock(spec=Player)

    alice_mock.name = 'Alice'
    alice_mock.piece = 'X'

    bob_mock.name = 'Bob'
    bob_mock.piece = 'O'

    game = Game(board=board, player1=alice_mock, player2=bob_mock)

    alice_mock.get_move.side_effect = [[0, 0], [0, 1], [2, 2], [2, 0], [1, 2]]
    bob_mock.get_move.side_effect = [[1, 0], [1, 1], [0, 2], [2, 1]]

    game.start()

    captured = capsys.readouterr()

    assert 'It\'s a cats game' in captured.out
