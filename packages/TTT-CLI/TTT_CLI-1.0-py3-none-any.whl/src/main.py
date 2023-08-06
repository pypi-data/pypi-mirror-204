from .tic_tac_toe import Game, Board, Player


def main():
    board = Board()
    player1 = Player(name='Player 1', piece='X')
    player2 = Player(name='Player 2', piece='O')
    game = Game(board=board, player1=player1, player2=player2)
    game.start()


if __name__ == '__main__':
    main()
