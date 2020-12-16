def read_blocks(filepath):
    tickets_file = open(filepath, "r")
    blocks = tickets_file.read().split("\n\n")
    tickets_file.close()

    return blocks


def extract_my_ticket(block):
    return list(map(int, block.split("\n")[1].split(",")))


def extract_rules(rules_block, num_positions):
    rules = dict()
    for rule in rules_block.split("\n"):
        rule_parts = rule.split(": ")
        key = rule_parts[0]
        ranges_part = rule_parts[1].split(" or ")
        single_valid_values = set()
        for single_range in ranges_part:
            single_range_parts = single_range.split('-')
            single_valid_values.update(list(range(int(single_range_parts[0]), int(single_range_parts[1]) + 1)))

        rules[key] = {"values": single_valid_values, "position": list(range(0, num_positions))}

    return rules


def get_valid_values(rules):
    valid_values = set()
    for key in rules:
        valid_values.update(rules[key]["values"])

    return valid_values


def get_not_valid_values(tickets_block, rules):
    tickets = tickets_block.split("\n")
    del tickets[0]
    valid_values = get_valid_values(rules)
    not_valid_values_in_tickets = []
    for ticket in tickets:
        ticket_arr = list(map(int, ticket.split(",")))
        for field_number in ticket_arr:
            if field_number not in valid_values:
                not_valid_values_in_tickets.append(field_number)

    return not_valid_values_in_tickets


def get_valid_tickets(tickets_block, not_valid_values):
    tickets = tickets_block.split("\n")
    del tickets[0]
    valid_tickets = []
    for ticket in tickets:
        ticket_arr = list(map(int, ticket.split(",")))
        include = True
        for field_number in ticket_arr:
            if field_number in not_valid_values:
                include = False
                break

        if include:
            valid_tickets.append(ticket_arr)

    return valid_tickets


def get_scanning_error_rate(filepath):
    blocks = read_blocks(filepath)
    my_ticket = extract_my_ticket(blocks[1])
    rules = extract_rules(blocks[0], len(my_ticket))
    not_valid_values_in_tickets = get_not_valid_values(blocks[2], rules)

    return sum(not_valid_values_in_tickets)


def remove_position_from_other_keys(rules, except_key, position_to_remove):
    for other_key in rules:
        if not other_key == except_key and position_to_remove in rules[other_key]["position"]:
            rules[other_key]["position"].remove(position_to_remove)


def process_is_finished(rules):
    for key in rules:
        if len(rules[key]["position"]) > 1:
            return False

    return True


def eval_departure_fields(rules, my_ticket):
    result = 1
    for key in rules:
        if key.startswith("departure"):
            result *= my_ticket[rules[key]["position"][0]]

    return result


def get_value_in_departure_fields(filepath):
    blocks = read_blocks(filepath)
    my_ticket = extract_my_ticket(blocks[1])
    rules = extract_rules(blocks[0], len(my_ticket))
    not_valid_values_in_tickets = get_not_valid_values(blocks[2], rules)
    valid_tickets = get_valid_tickets(blocks[2], not_valid_values_in_tickets)

    for ticket in valid_tickets:
        for i in range(0, len(ticket)):
            for key in rules:
                if ticket[i] not in rules[key]["values"]:
                    if i in rules[key]["position"]:
                        rules[key]["position"].remove(i)

                if len(rules[key]["position"]) == 1:
                    remove_position_from_other_keys(rules, key, rules[key]["position"][0])

        if process_is_finished(rules):
            break

    return eval_departure_fields(rules, my_ticket)


# ASSERTS
assert get_scanning_error_rate('../inputs/test.txt') == 71

print("Part one: " + str(get_scanning_error_rate('../inputs/input.txt')))
print("Part two: " + str(get_value_in_departure_fields('../inputs/input.txt')))
