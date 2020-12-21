ACTIVE = "#"
INACTIVE = "."


class Game:
    def __init__(self, filepath, is4d):
        self.next_active_cubes = set()
        self.is4d = is4d
        self.active_cubes = self.__read_input(filepath)

    def play(self, cycles):
        for i in range(0, cycles):
            self.__play_cycle()

        return len(self.active_cubes)

    def __play_cycle(self):
        cubes_processed = set()
        next_active_cubes = set()

        for cube in self.active_cubes:
            neighbors = self.__get_neighbors(cube)
            neighbors.add(cube)

            for neighbor in neighbors:
                if neighbor in cubes_processed:
                    continue

                cubes_processed.add(neighbor)
                actives = 0
                for next_neighbour in self.__get_neighbors(neighbor):
                    if next_neighbour in self.active_cubes:
                        actives += 1

                if (actives in [2, 3] and neighbor in self.active_cubes) or (
                        neighbor not in self.active_cubes and actives == 3):
                    next_active_cubes.add(neighbor)

        self.active_cubes = next_active_cubes

    def __read_input(self, filepath):
        game_file = open(filepath, "r")
        lines = game_file.read().splitlines()
        game_file.close()

        active_cubes = set()
        for y in range(0, len(lines)):
            for x in range(0, len(lines[y])):
                if lines[y][x] == ACTIVE:
                    if self.is4d:
                        active_cubes.add((x, y, 0, 0))
                    else:
                        active_cubes.add((x, y, 0))

        return active_cubes

    def __get_neighbors(self, cube):
        neighbors = set()
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                for z in [-1, 0, 1]:
                    if self.is4d:
                        for w in [-1, 0, 1]:
                            self.__add_neigbor(cube, (cube[0] + x, cube[1] + y, + cube[2] + z, + cube[3] + w),
                                               neighbors)
                    else:
                        self.__add_neigbor(cube, (cube[0] + x, cube[1] + y, + cube[2] + z), neighbors)

        return neighbors

    def __add_neigbor(self, cube, neighbor_coords, neighbors):
        if not neighbor_coords == cube:
            neighbors.add(neighbor_coords)


def play(filepath, cycles, is4d):
    game = Game(filepath, is4d)
    return game.play(cycles)


## Asserts
assert play('../inputs/test.txt', 6, False) == 112
assert play('../inputs/test.txt', 6, True) == 848

print('Part one: ' + str(play('../inputs/input.txt', 6, False)))
print('Part two: ' + str(play('../inputs/input.txt', 6, True)))
