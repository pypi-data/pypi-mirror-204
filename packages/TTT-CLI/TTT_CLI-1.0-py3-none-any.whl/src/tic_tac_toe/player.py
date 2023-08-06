class Player:

    def __init__(self, name, piece):
        self.name = name
        self.piece = piece

    def get_move(self):
        print('Where would you like to place your piece?')
        move = input('enter row and col separated by spaces: ')
        return list(map(int, move.split(' ')))
