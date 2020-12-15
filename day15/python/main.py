def init_game_history(numbers):
    game_history = {}
    turn = 1
    for number in numbers:
        init_number_history(number, game_history, turn)
        turn += 1

    return game_history


def read_numbers(filepath):
    notes_file = open(filepath, "r")

    lines = notes_file.read().splitlines()
    rounds = []
    for i in range(0, len(lines)):
        rounds.append(list(map(int, lines[i].split(','))))

    notes_file.close()
    return rounds

def init_number_history(number, game_history, turn):
    game_history[number] = {'turn': turn, 'turn_previous': turn, 'times': 1}

def play_rounds(filepath, times_per_round):
    rounds = read_numbers(filepath)
    results = []

    for single_round in rounds:
        result = play_round(single_round, times_per_round)
        print(str(single_round) + ' -> ' + str(result))
        results.append(result)

    return results


def play_round(initial_numbers, times_per_round):
    game_history = init_game_history(initial_numbers)
    last_number_spoken = initial_numbers[len(initial_numbers) - 1]
    for turn in range(len(initial_numbers) + 1, times_per_round + 1):
        last_number_spoken_history = game_history[last_number_spoken]
        if last_number_spoken_history['times'] == 1:
            last_number_spoken = 0
        else:
            last_number_spoken = last_number_spoken_history['turn'] - last_number_spoken_history['turn_previous']

        if last_number_spoken not in game_history:
            init_number_history(last_number_spoken, game_history, turn)
        else:
            current_number_spoken_history = game_history[last_number_spoken]
            current_number_spoken_history['times'] += 1
            current_number_spoken_history['turn_previous'] = current_number_spoken_history['turn']
            current_number_spoken_history['turn'] = turn

    return last_number_spoken


EXPECTED_RESULTS_WITH_2020_TIMES_PER_ROUND = [436, 1, 10, 27, 78, 438, 1836]
print(' ------ INIT: Asserts part one -----------')
results = play_rounds('../inputs/test.txt', 2020)
for i in range(0, len(results)):
    assert results[i] == EXPECTED_RESULTS_WITH_2020_TIMES_PER_ROUND[i]

print(' ------ END: Asserts part one -----------')

EXPECTED_RESULTS_WITH_30000000_TIMES_PER_ROUND = [175594, 2578, 3544142, 261214, 6895259, 18, 362]
print(' ------ INIT: Asserts part two -----------')
results = play_rounds('../inputs/test.txt', 30000000)
for i in range(0, len(results)):
     assert results[i] == EXPECTED_RESULTS_WITH_30000000_TIMES_PER_ROUND[i]
print(' ------ END: Asserts part two -----------')

print('Part one: ' + str(play_rounds('../inputs/input.txt', 2020)[0]))
print('Part two: ' + str(play_rounds('../inputs/input.txt', 30000000)[0]))