class Ship:
    DIRECTIONS = ['N', 'E', 'S', 'W']

    def __init__(self, current_direction):
        self.position_x = 0
        self.position_y = 0
        self.current_direction = current_direction
        self.waypoint = Waypoint(10, 1)

    def navigate(self, instructions, use_waypoint):
        navigation_method = self.__without_waypoint
        if use_waypoint:
            navigation_method = self.__with_waypoint
        for instruction in instructions:
            navigation_method(instruction['action'], instruction['value'])

        return [self.position_x, self.position_y]

    def __without_waypoint(self, action, instruction_value):
        if action == 'F':
            self.__move_forward(instruction_value)
        elif action == 'R':
            self.__turn_right(instruction_value)
        elif action == 'L':
            self.__turn_left(instruction_value)
        elif action in self.DIRECTIONS:
            self.__move(action, instruction_value)

        return [self.position_x, self.position_y]

    def __with_waypoint(self, action, instruction_value):
        if action == 'F':
            self.__move_forward_to_waypoint(instruction_value)
        elif action in ['R', 'L']:
            self.__rotate_waypoint(action, instruction_value)
        elif action in self.DIRECTIONS:
            self.__move_waypoint(action, instruction_value)

    def __move_forward(self, units):
        self.__move(self.current_direction, units)

    def __move(self, direction, units):
        if direction == 'E':
            self.position_x += units
        elif direction == 'W':
            self.position_x -= units
        elif direction == 'N':
            self.position_y += units
        elif direction == 'S':
            self.position_y -= units

    def __turn_right(self, degrees):
        units_to_move = int(degrees / 90)
        current_index = self.DIRECTIONS.index(self.current_direction)
        self.current_direction = self.DIRECTIONS[(units_to_move + current_index) % 4]

    def __turn_left(self, degrees):
        units_to_move = int(degrees / 90)
        current_index = self.DIRECTIONS.index(self.current_direction)
        self.current_direction = self.DIRECTIONS[(current_index - units_to_move) % 4]

    def __move_forward_to_waypoint(self, units):
        self.position_x += (units * self.waypoint.position_x)
        self.position_y += (units * self.waypoint.position_y)

    def __move_waypoint(self, direction, units):
        self.waypoint.move(direction, units)

    def __rotate_waypoint(self, direction, degress):
        if direction == 'R':
            self.waypoint.rotate_right(degress)
        else:
            self.waypoint.rotate_left(degress)


class Waypoint:
    def __init__(self, start_x, start_y):
        self.position_x = start_x
        self.position_y = start_y

    def move(self, direction, units):
        if direction == 'E':
            self.position_x += units
        elif direction == 'W':
            self.position_x -= units
        elif direction == 'N':
            self.position_y += units
        elif direction == 'S':
            self.position_y -= units

    def rotate_right(self, degrees):
        units_to_move = int(degrees / 90)
        for i in range(0, units_to_move):
            self.position_x, self.position_y = self.position_y, -self.position_x

    def rotate_left(self, degrees):
        units_to_move = int(degrees / 90)
        for i in range(0, units_to_move):
            self.position_x, self.position_y = -self.position_y, self.position_x


def read_instructions(filepath):
    read_instructions_file = open(filepath, "r")
    lines = read_instructions_file.read().splitlines()

    instructions = []
    for line in lines:
        instructions.append({'action': line[0], 'value': int(line[1:])})

    return instructions


def calc_manhattan_distance(instructions_file, initial_direction, use_waypoint):
    ship = Ship(initial_direction)
    coords = ship.navigate(read_instructions(instructions_file), use_waypoint)

    return abs(coords[0]) + abs(coords[1])


assert calc_manhattan_distance('../inputs/test.txt', 'E', False) == 25
assert calc_manhattan_distance('../inputs/test.txt', 'E', True) == 286

print('Part one: ' + str(calc_manhattan_distance('../inputs/input.txt', 'E', False)))
print('Part two: ' + str(calc_manhattan_distance('../inputs/input.txt', 'E', True)))
