def read_joltage_ratings(filepath):
    adapters_joltage_ratings_file = open(filepath, "r")
    adapters_joltage_ratings = list(map(int, adapters_joltage_ratings_file.read().splitlines()))
    adapters_joltage_ratings.sort()
    adapters_joltage_ratings_file.close()

    return adapters_joltage_ratings


def get_built_in_joltage_adapter(adapters_joltage_ratings, joltage_built_in_rated):
    return max(adapters_joltage_ratings) + joltage_built_in_rated


def eval_part(adapters_joltage_ratings_file, charging_outlet_effective_rating, built_in_joltage_adapter):
    charging_effective_rating = charging_outlet_effective_rating
    adapters_joltage_ratings = read_joltage_ratings(adapters_joltage_ratings_file)
    adapters_joltage_ratings.append(get_built_in_joltage_adapter(adapters_joltage_ratings, built_in_joltage_adapter))

    adapter_1_jolt = []
    adapter_3_jolt = []
    for adapter_joltage_rated in adapters_joltage_ratings:
        if adapter_joltage_rated - 1 == charging_effective_rating:
            adapter_1_jolt.append(adapter_joltage_rated)
            charging_effective_rating = adapter_joltage_rated
        else:
            if adapter_joltage_rated - 3 == charging_effective_rating:
                adapter_3_jolt.append(adapter_joltage_rated)
            charging_effective_rating = adapter_joltage_rated

    return len(adapter_1_jolt) * len(adapter_3_jolt)


def count_distinct_arrangements(adapters_joltage_ratings_file):
    adapters_joltage_ratings = read_joltage_ratings(adapters_joltage_ratings_file)
    max_jolt = max(adapters_joltage_ratings)
    arrangements = [0] * (max_jolt + 1)
    arrangements[0] = 1
    for i in range(3, max_jolt + 1):
        for j in range(0, 3):
            key = i - j
            if key in adapters_joltage_ratings:
                arrangements[key] = arrangements[key - 1] + arrangements[key - 2] + arrangements[key - 3]

    return arrangements[max_jolt]


def get_distinct_arrangements(adapters_joltage_ratings_file, built_in_joltage_adapter):
    adapters_joltage_ratings = read_joltage_ratings(adapters_joltage_ratings_file)
    adapters_joltage_ratings.append(get_built_in_joltage_adapter(adapters_joltage_ratings, built_in_joltage_adapter))
    trees = []
    build_tree(adapters_joltage_ratings, built_in_joltage_adapter, trees, max(adapters_joltage_ratings))

    return len(trees)


## Asserts
assert eval_part('../inputs/test.txt', 0, 3) == 35
assert eval_part('../inputs/test2.txt', 0, 3) == 220
assert count_distinct_arrangements('../inputs/test.txt') == 8
assert count_distinct_arrangements('../inputs/test2.txt') == 19208

print('Part one: ' + str(eval_part('../inputs/input.txt', 0, 3)))
print('Part one: ' + str(count_distinct_arrangements('../inputs/input.txt')))
