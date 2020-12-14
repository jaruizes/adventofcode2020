def read_notes(filepath):
    notes_file = open(filepath, "r")
    lines = notes_file.read().splitlines()
    earliest_timestamp = int(lines[0])
    bus_ids = lines[1].split(',')

    return [earliest_timestamp, bus_ids]


def get_earliest_bus_multiplied_by_minutes_to_timestamp(filepath):
    notes = read_notes(filepath)
    earliest_timestamp = notes[0]
    earliest_bus_id = 0
    minutes_to_timestamp = 999999999
    for bus_id in notes[1]:
        if not bus_id == 'x':
            minutes_past_timestamp = int(bus_id) * ceil(earliest_timestamp / int(bus_id)) - earliest_timestamp
            if minutes_past_timestamp < minutes_to_timestamp:
                minutes_to_timestamp = minutes_past_timestamp
                earliest_bus_id = bus_id

    return int(earliest_bus_id) * int(minutes_to_timestamp)


def get_earliest_timestamp_match(filepath):
    notes = read_notes(filepath)
    bus_ids = []

    for i in range(0, len(notes[1])):
        if not notes[1][i] == 'x':
            bus_ids.append(int(notes[1][i]))

    timestamp_found = False
    time = 0
    increment = 1
    while not timestamp_found:
        iteration_matches = []
        time += increment

        for bus_id in bus_ids:
            bus_increment_time_depart = notes[1].index(str(bus_id))
            if not ((time + bus_increment_time_depart) % bus_id) == 0:
                break
            else:
                iteration_matches.append(bus_id)
                increment = int((bus_id * increment) / mcd(bus_id, increment))
                if len(iteration_matches) == len(bus_ids):
                    timestamp_found = True
                    break

    return time


def mcd(x, y):
    while y > 0:
        rest = y
        y = x % y
        x = rest
    return x


assert get_earliest_bus_multiplied_by_minutes_to_timestamp('../inputs/test.txt') == 295
assert get_earliest_timestamp_match('../inputs/test.txt') == 1068781

print('Part one: ' + str(get_earliest_bus_multiplied_by_minutes_to_timestamp('../inputs/input.txt')))
print('Part two: ' + str(get_earliest_timestamp_match('../inputs/input.txt')))