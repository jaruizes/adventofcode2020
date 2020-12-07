def read_rules(filepath):
    rules_file = open(filepath, "r")
    rules = rules_file.read().splitlines()
    rules_file.close()
    return rules


def build_dict(rules):
    rules_dict = {}
    for rule in rules:
        parts = rule.split('bags contain')
        key = parts[0].strip()
        values = parts[1].replace(' bags', '').replace(' bag', '').replace('.', '').strip().split(', ')
        values_detailed = {}
        for value in values:
            first_space = value.index(' ')
            value_amount = value[0: first_space]
            value_key = value[first_space + 1:]
            values_detailed[value_key] = value_amount

        rules_dict[key] = values_detailed

    return rules_dict


def get_possibilities(rules_dict, target):
    total = 0
    for key in rules_dict:
        values = rules_dict[key]
        found = int(eval_bag(values, target, rules_dict))
        if found > 0:
            total += 1

    return total


def eval_bag(values, target, rules_dict):
    if target in values:
        return values[target]

    for value in values:
        if not value == 'other':
            found = int(eval_bag(rules_dict[value], target, rules_dict))
            if found > 0:
                return found

    return 0


def count_bags(rules_dict, start):
    values = rules_dict[start]
    total = 0

    for key in values:
        value = values[key]
        if type(value) is not dict:
            if not key == 'other':
                total += int(value) + int(value) * int(count_bags(rules_dict, key))
        else:
            total += int(count_bags(rules_dict, key))

    return total


## Asserts
assert count_bags(build_dict(read_rules('../inputs/test.txt')), 'shiny gold') == 32
assert count_bags(build_dict(read_rules('../inputs/test2.txt')), 'shiny gold') == 126

print('Part one: ' + str(get_possibilities(build_dict(read_rules('../inputs/input.txt')), 'shiny gold')))
print('Part two: ' + str(count_bags(build_dict(read_rules('../inputs/input.txt')), 'shiny gold')))
