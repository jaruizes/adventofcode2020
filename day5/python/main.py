def init_values(max_value):
    i = 0
    seats = []
    while i < max_value:
        seats.append(i)
        i += 1

    return seats


def readfile(filepath):
    """
    This function reads the file associated with filename and returns a list of patterns

    :param filepath: The path of the file containing the list of numbers
    :return: returns list of patterns
    """
    file_obj = open(filepath, "r")
    patterns = file_obj.read().splitlines()
    file_obj.close()
    return patterns


def process_pattern(pattern, values):
    for letter in pattern:
        if letter == 'F' or letter == 'L':
            set_of_seats = get_lower_half(values)
        if letter == 'B' or letter == 'R':
            set_of_seats = get_upper_half(values)

        values = values[set_of_seats[0]: set_of_seats[1]]

    return values


def get_lower_half(values):
    middle = int(len(values) / 2)
    return [0, middle]


def get_upper_half(values):
    middle = int(len(values) / 2)
    return [middle, len(values)]


def get_row(pattern):
    return process_pattern(pattern[0:7], init_values(128))[0]


def get_column(pattern):
    return process_pattern(pattern[7:10], init_values(8))[0]


def get_seat(row, colum):
    return (row * 8) + colum


def get_seats(filepath) -> list:
    patterns = readfile(filepath)
    seats = []
    for pattern in patterns:
        row = get_row(pattern)
        column = get_column(pattern)
        current_seat = get_seat(row, column)

        seats.append(current_seat)

    return seats


def get_my_current_seat(seats):
    seats.sort()

    for i in range(len(seats)):
        current_seat = seats[i]
        next_seat = seats[i+1]

        if next_seat - current_seat == 2:
            return current_seat + 1


## Asserts
assert max(get_seats('../inputs/test.txt')) == 820

print('Part one: ' + str(max(get_seats('../inputs/input.txt'))))
print('Part two: ' + str(get_my_current_seat(get_seats('../inputs/input.txt'))))
