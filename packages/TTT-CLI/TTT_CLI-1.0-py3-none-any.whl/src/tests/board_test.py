from ..tic_tac_toe import Board


def test_board_initialize():
    num_rows = 3
    board = Board(num_rows)

    assert board.num_rows == num_rows
    assert len(board.grid) == num_rows
    assert all(len(row) == num_rows for row in board.grid)


def test_board_getitem_and_setitem():
    piece = 'X'
    board = Board(3)
    board[0, 0] = piece

    assert board[0, 0] == piece


def test_board_str():
    board = Board(3)

    assert str(
        board) == '  |   |  \n---------\n  |   |  \n---------\n  |   |  '


def has_win_condition():
    # has horizontal win
    board = Board(3)
    board[0, 0] = 'X'
    board[0, 1] = 'X'
    board[0, 2] = 'X'

    assert board.has_win_condition()

    # has vertical win
    board = Board(3)
    board[0, 0] = 'X'
    board[1, 0] = 'X'
    board[2, 0] = 'X'

    assert board.has_win_condition()

    board = Board(3)
    board[0, 0] = 'X'
    board[1, 1] = 'X'
    board[2, 2] = 'X'

    assert board.has_win_condition()

    board = Board(3)
    board[0, 2] = 'X'
    board[1, 1] = 'X'
    board[0, 2] = 'X'

    assert board.has_win_condition()


def test_board_is_full():
    board = Board(2)
    assert not board.is_full()

    board[0, 0] = 'X'
    board[0, 1] = 'O'
    board[1, 0] = 'S'
    board[1, 1] = 'P'

    assert board.is_full()
