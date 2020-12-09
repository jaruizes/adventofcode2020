def read_message_file(filepath):
    message_file = open(filepath, "r")
    message = list(map(int, message_file.read().splitlines()))
    message_file.close()
    return message


def eval_sums_preamble(preamble):
    sums = []
    preamble_without_duplicates = list(dict.fromkeys(preamble))
    for i in range(len(preamble_without_duplicates)):
        rest = preamble_without_duplicates.copy()
        current = int(preamble_without_duplicates[i])
        del rest[i]
        for number in rest:
            result = int(number) + current
            if result not in sums:
                sums.append(result)

    return sums


def find_weakness(filepath, preamble_length):
    message = read_message_file(filepath)
    preamble_start = 0
    preamble_end = preamble_length

    while preamble_end < len(message):
        preamble = message[preamble_start: preamble_end]
        current_number = message[preamble_end]
        preamble_sums = eval_sums_preamble(preamble)
        if current_number not in preamble_sums:
            return current_number

        preamble_start += 1
        preamble_end += 1

    return -1


def find_set_of_numbers(filepath, target, preamble_length):
    message = read_message_file(filepath)
    set_found = eval_window(target, message, preamble_length)
    if set_found:
        return min(set_found) + max(set_found)

    return -1


def eval_window(target, message, preamble_length):
    preamble_start = 0
    preamble_end = preamble_start + preamble_length

    preamble = []
    found = False
    while preamble_end < len(message):
        preamble = message[preamble_start: preamble_end]
        if target == sum(preamble):
            found = True
            break

        preamble_start += 1
        preamble_end += 1

    if not found:
        preamble_length += 1
        preamble = eval_window(target, message, preamble_length)

    return preamble


## Asserts
assert find_weakness('../inputs/test.txt', 5) == 127
assert find_set_of_numbers('../inputs/test.txt', find_weakness('../inputs/test.txt', 5), 2) == 62

print('Part one: ' + str(find_weakness('../inputs/input.txt', 25)))
print('Part two: ' + str(find_set_of_numbers('../inputs/input.txt', find_weakness('../inputs/input.txt', 25), 2)))
