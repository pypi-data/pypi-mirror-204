class Game:

    def __init__(self, board, player1, player2):
        self.board = board
        self.player1 = player1
        self.player2 = player2

    def start(self):
        current_player = self.player1

        while True:
            print(self.board)
            row, col = current_player.get_move()
            print(f'row {row}, col {col}, piece {current_player.piece}')

            self.board[row, col] = current_player.piece

            if self.board.has_win_condition():
                print(f'Player {current_player.name} wins!')
                print(self.board)
                return
            if self.board.is_full():
                print('It\'s a cats game')
                print(self.board)
                return

            if current_player == self.player1:
                current_player = self.player2
            else:
                current_player = self.player1
