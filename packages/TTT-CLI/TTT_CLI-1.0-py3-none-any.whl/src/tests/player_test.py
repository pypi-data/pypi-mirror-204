from ..tic_tac_toe import Player


def test_player_initialization():
    p = Player('Alice', 'X')
    assert p.name == 'Alice'
    assert p.piece == 'X'


def test_player_get_move(monkeypatch):
    with monkeypatch.context() as m:
        m.setattr('builtins.input', lambda _: '1 2')
        p = Player('Alice', 'X')

        assert p.get_move() == [1, 2]
