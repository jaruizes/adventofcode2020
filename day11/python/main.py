class Seat:
    def __init__(self, x, y, seat_type):
        self.x = x
        self.y = y
        self.seat_type = seat_type
        self.status = seat_type
        self.potential_status = seat_type
        self.last_status = seat_type

    def fill(self):
        self.potential_status = '#'

    def release(self):
        self.potential_status = 'L'

    def consolidate(self):
        self.last_status = self.status
        self.status = self.potential_status

    def is_empty(self):
        return self.status == 'L'

    def is_occupied(self):
        return self.status == '#'

    def is_status_changed(self):
        return not self.status == self.last_status


def read_seat_layout(filepath):
    seat_layout_file = open(filepath, "r")
    lines = seat_layout_file.readlines()

    y = 0
    seats = []
    for line in lines:
        content = line.strip()
        seats_in_row = []
        for x in range(len(content)):
            seat = Seat(x, y, content[x])
            seats_in_row.append(seat)

        y += 1

        seats.append(seats_in_row)

    seat_layout_file.close()

    return seats

def get_seats_adjacent(seats, seat_x, seat_y):
    seats_adjacent = []
    for x in range(seat_x - 1, seat_x + 2):
        if 0 <= x < len(seats[0]):
            for y in range(seat_y - 1, seat_y + 2):
                if 0 <= y < len(seats):
                    if not x == seat_x or not y == seat_y:
                        seat = seats[y][x]
                        if not seat.seat_type == '.':
                            seats_adjacent.append(seat.status)

    return seats_adjacent

def eval_seats_can_see(seats, seat_x, seat_y):
    seats_adjacent = []

    ## Row ->
    for x in range(seat_x + 1, len(seats[0])):
        seat_adjacent = seats[seat_y][x]
        if not seat_adjacent.seat_type == '.':
            seats_adjacent.append(seat_adjacent.status)
            break

    ## Row <-
    for x in range(seat_x - 1, -1, -1):
        seat_adjacent = seats[seat_y][x]
        if not seat_adjacent.seat_type == '.':
            seats_adjacent.append(seat_adjacent.status)
            break

    ## Column ^
    for y in range(seat_y + 1, len(seats)):
        seat_adjacent = seats[y][seat_x]
        if not seat_adjacent.seat_type == '.':
            seats_adjacent.append(seat_adjacent.status)
            break

    ## Column down
    for y in range(seat_y - 1, -1, -1):
        seat_adjacent = seats[y][seat_x]
        if not seat_adjacent.seat_type == '.':
            seats_adjacent.append(seat_adjacent.status)
            break

    ## Diagonal up - right
    x = seat_x + 1
    y = seat_y - 1
    while x < len(seats[0]) and y >= 0:
        seat_adjacent = seats[y][x]
        if not seat_adjacent.seat_type == '.':
            seats_adjacent.append(seat_adjacent.status)
            break
        x += 1
        y -= 1

    ## Diagonal down - right
    x = seat_x + 1
    y = seat_y + 1
    while x < len(seats[0]) and y < len(seats):
        seat_adjacent = seats[y][x]
        if not seat_adjacent.seat_type == '.':
            seats_adjacent.append(seat_adjacent.status)
            break

        x += 1
        y += 1

    ## Diagonal up - left
    x = seat_x - 1
    y = seat_y - 1
    while x >= 0 and y >= 0:
        seat_adjacent = seats[y][x]
        if not seat_adjacent.seat_type == '.':
            seats_adjacent.append(seat_adjacent.status)
            break

        x -= 1
        y -= 1

    ## Diagonal down - left
    x = seat_x - 1
    y = seat_y + 1
    while x >= 0 and y < len(seats):
        seat_adjacent = seats[y][x]
        if not seat_adjacent.seat_type == '.':
            seats_adjacent.append(seat_adjacent.status)
            break

        x -= 1
        y += 1

    return seats_adjacent


def consolidate(seats):
    no_changes = True
    for row in seats:
        for seat in row:
            seat.consolidate()
            if seat.is_status_changed():
                no_changes = False

    return no_changes


def apply_rules(seats, seats_adjacent_function, limit_occupied):
    for row in seats:
        for seat in row:
            apply_ruleset(seats, seat, seats_adjacent_function, limit_occupied)

    return seats


def apply_ruleset(seats, seat, seats_adjacent_function, limit_occupied):
    if not seat.seat_type == '.':
        seats_adjacent = seats_adjacent_function(seats, seat.x, seat.y)
        all_seats_adjacent_are_empty = seats_adjacent.count('L') == len(seats_adjacent)

        if seat.is_empty() and all_seats_adjacent_are_empty:
            seat.fill()
        else:
            seats_adjacent_occupied = seats_adjacent.count('#')
            if seat.is_occupied() and seats_adjacent_occupied >= limit_occupied:
                seat.release()


def find_seats_occupied(seats_file, seats_adjacent_function, limit_occupied):
    seats = read_seat_layout(seats_file)
    no_changes = False
    occupied = 0

    while not no_changes:
        apply_rules(seats, seats_adjacent_function, limit_occupied)
        no_changes = consolidate(seats)

    for row in seats:
        for seat in row:
            if seat.is_occupied():
                occupied += 1

    return occupied


assert find_seats_occupied('../inputs/test.txt', get_seats_adjacent, 4) == 37
assert find_seats_occupied('../inputs/test.txt', eval_seats_can_see, 5) == 26

print('Part one: ' + str(find_seats_occupied('../inputs/input.txt', get_seats_adjacent, 4)))
print('Part two: ' + str(find_seats_occupied('../inputs/input.txt', eval_seats_can_see, 5)))
