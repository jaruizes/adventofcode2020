class Game:
    def __init__(self, definition_file):
        self.board = self.__read_board(definition_file)
        self.x = 0
        self.y = 0
        self.trees = 0
        self.finished = False

    def move(self, offset_x, offset_y):
        self.x += offset_x
        while self.x > len(self.board[0]) - 1:
            self.__expand_board()

        self.y += offset_y
        if self.y > len(self.board) - 1:
            self.finished = True
            return

        row = self.board[self.y]
        if row[self.x] == '#':
            self.trees += 1

        return

    def is_finished(self):
        return self.finished

    def count_trees(self):
        return self.trees

    def __expand_board(self):
        expanded_board = []
        for row in self.board:
            expanded_board.append(row + row)

        self.board = expanded_board

    def __read_board(self, definition_file):
        file = open(definition_file, "r")
        board = file.read().splitlines()
        file.close()
        return board


def multiply(trees_founds_in_games):
    """
    This function multiplies the numbers in trees

    :param trees_founds_in_games: set of trees found
    :return: result of the product
    """
    total = 1
    for trees in trees_founds_in_games:
        total = total * trees

    return total


def play(definition_file, movements, result_function):
    trees = []
    for movement in movements:
        game = Game(definition_file)
        offset_x = movement[0]
        offset_y = movement[1]

        while not game.is_finished():
            game.move(offset_x, offset_y)

        trees.append(game.count_trees())

    return result_function(trees)


## Asserts
assert play('../inputs/test.txt', [[3, 1]], multiply) == 7
assert play('../inputs/test.txt', [[1, 1], [3, 1], [5, 1], [7, 1], [1, 2]], multiply) == 336

print('Part one: ', play('../inputs/input.txt', [[3, 1]], multiply))
print('Part two: ', play('../inputs/input.txt', [[1, 1], [3, 1], [5, 1], [7, 1], [1, 2]], multiply))
