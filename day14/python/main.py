def read_instructions(filepath, apply_mask_to_value, apply_mask_to_memory):
    instructions_file = open(filepath, "r")
    lines = instructions_file.read().splitlines()
    instructions = {}
    commands = []
    mask = ""

    for i in range(0, len(lines)):
        line = lines[i]
        memory_positions = []
        if line.startswith('mask'):
            mask = line.split(" = ")[1]
        else:
            instruction_parts = line.split(" = ")
            memory_position = int(instruction_parts[0].replace("mem[", "").replace("]", ""))
            if apply_mask_to_memory:
                memory_positions = get_memory_addresses(apply_mask_decoder(mask, decimal_to_binary(memory_position)))
            else:
                memory_positions.append(memory_position)

            instruction_value = int(instruction_parts[1])
            binary_value = decimal_to_binary(instruction_value)
            if apply_mask_to_value:
                binary_value = apply_mask(mask, binary_value)

            commands.append([memory_positions, binary_value])

    instructions_file.close()
    instructions['commands'] = commands

    return instructions


def decimal_to_binary(n):
    return (bin(n).replace("0b", "")).zfill(36)


def binary_to_decimal(n):
    return int(n, 2)


def apply_mask(mask, binary_number):
    binary_number_list = list(binary_number)
    for i in range(0, len(mask)):
        if not mask[i] == 'X':
            binary_number_list[i] = mask[i]

    return "".join(binary_number_list)


def apply_mask_decoder(mask, binary_number):
    binary_number_list = list(binary_number)
    for i in range(0, len(mask)):
        if not mask[i] == '0':
            binary_number_list[i] = mask[i]

    return "".join(binary_number_list)


def get_memory_addresses(binary_number):
    number_of_x = binary_number.count('X')
    possibilities = pow(2, number_of_x)
    addresses = []

    for i in range(0, possibilities):
        address = binary_number
        binary = decimal_to_binary(i)
        for possibility in list(binary[len(binary) - number_of_x:]):
            address = address.replace('X', possibility, 1)

        decimal = binary_to_decimal(address)
        if decimal not in addresses:
            addresses.append(decimal)

    return addresses


def initialize_memory(filepath, apply_mask_to_value, apply_mask_to_memory):
    instructions = read_instructions(filepath, apply_mask_to_value, apply_mask_to_memory)
    memory = {}

    for command in instructions['commands']:
        for memory_pos in command[0]:
            memory[memory_pos - 1] = binary_to_decimal(command[1])

    total = 0
    for pos in memory:
        total += memory[pos]

    return total


assert initialize_memory('../inputs/test.txt', True, False) == 165
assert initialize_memory('../inputs/test2.txt', False, True) == 208

print('Part one: ' + str(initialize_memory('../inputs/input.txt', True, False)))
print('Part two: ' + str(initialize_memory('../inputs/input.txt', False, True)))
