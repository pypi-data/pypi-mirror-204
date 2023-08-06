class Board():

    def __init__(self, num_rows=3):
        self.num_rows = num_rows
        self.grid = [[None] * self.num_rows for _ in range(self.num_rows)]

    def __getitem__(self, index):
        row, col = index

        return self.grid[row][col]

    def __setitem__(self, index, value):
        row, col = index
        self.grid[row][col] = value

    def __str__(self):
        rows = []
        for row in self.grid:
            row_str = ' | '.join([val or ' ' for val in row])
            rows.append(row_str)
        separator = '\n' + '-' * 9 + '\n'
        return separator.join(rows)

    def has_win_condition(self):
        return (self.__has_horizontal_win() or self.__has_vertical_win()
                or self.__has_diagonal_win())

    def is_full(self):
        return all(map(all, self.grid))

    def __has_horizontal_win(self):
        return any(row[0] and all(cell == row[0] for cell in row)
                   for row in self.grid)

    def __has_vertical_win(self):
        return any(row[0] and all(cell == row[0] for cell in row)
                   for row in zip(*self.grid))

    def __has_diagonal_win(self):
        diag1 = [self.grid[i][i] for i in range(self.num_rows)]
        diag2 = [self.grid[i][-i + 1] for i in range(self.num_rows)]

        def check_equality(diag):
            return diag[0] and all(cell == diag[0] for cell in diag)

        return any(map(check_equality, [diag1, diag2]))
